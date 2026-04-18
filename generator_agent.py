import os
from groq import Groq
from dotenv import load_dotenv
from utils import extract_json, validate_generator

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


# rough guide for how deep explanation should go
GRADE_GUIDE = [
    (range(1, 4), "Very simple words. Keep it short. Use daily life examples. Avoid technical terms."),
    (range(4, 7), "Simple language. Introduce basic terms slowly. Add 1-2 relatable examples."),
    (range(7, 10), "Use proper terms. Explain why things work. Add one example."),
    (range(10, 13), "Use technical language. Include formulas if needed. Don't oversimplify.")
]


def get_guidance(grade):
    try:
        g = int(grade)
    except:
        return "Explain according to student's level."

    for r, text in GRADE_GUIDE:
        if g in r:
            return text

    return "Explain according to student's level."


class GeneratorAgent:

    def __init__(self, retries=3):
        self.retries = retries

    def build_prompt(self, grade, topic, feedback=None):
        guide = get_guidance(grade)

        prompt = f"""
You are writing educational content.

Topic: {topic}
Grade: {grade}

Language rule: {guide}

Return ONLY JSON. No extra text.

Format:
{{
  "explanation": "...",
  "mcqs": [
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "answer": "..."
    }},
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "answer": "..."
    }},
    {{
      "question": "...",
      "options": ["...", "...", "...", "..."],
      "answer": "..."
    }}
  ]
}}

Rules:
- explanation should match grade level
- exactly 3 questions
- each question has 4 options
- answer must match one option exactly
- questions must come from explanation
"""

        if feedback:
            issues = "\n".join([f"- {f}" for f in feedback])
            prompt += f"""

Previous output had issues. Fix them:

{issues}

Do not repeat mistakes.
"""

        return prompt

    def run(self, grade, topic, feedback=None):
        prompt = self.build_prompt(grade, topic, feedback)

        for i in range(self.retries):
            print(f"[GEN] try {i+1}/{self.retries}")

            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1200,
                temperature=0.3
            )

            out = res.choices[0].message.content.strip()
            print("raw:\n", out, "\n")

            try:
                data = extract_json(out)
                return validate_generator(data)

            except Exception as err:
                print("error:", err)

                # retry with correction info
                prompt = f"""
Fix this JSON.

Error:
{err}

Previous output:
{out}

Return ONLY fixed JSON.
"""

        raise Exception("failed after retries")