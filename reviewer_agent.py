import os
import json
from groq import Groq
from dotenv import load_dotenv
from utils import extract_json, validate_reviewer

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


class ReviewerAgent:

    def __init__(self, retries=3):
        self.retries = retries

    def build_prompt(self, content, grade):
        content_str = json.dumps(content, indent=2)

        prompt = f"""
You are reviewing educational content.

Target grade: {grade}

Content:
{content_str}

Check these things:

1. Is it suitable for the grade?
   - too easy or too hard?
   - basic vs technical mismatch?

2. Is it correct?
   - facts right?
   - answers correct?
   - wrong options still believable?

3. Is it clear?
   - explanation understandable?
   - questions make sense?
   - options not confusing?

Also:
- questions should only come from explanation
- answer must exactly match one option
- explanation should not be too short

Decision:
- if anything is wrong → fail
- otherwise → pass

Return ONLY JSON:

{{
  "status": "pass",
  "feedback": []
}}

OR

{{
  "status": "fail",
  "feedback": ["issue 1", "issue 2"]
}}

Rules:
- status must be "pass" or "fail"
- feedback must be list
- if fail → at least one issue
- be specific
"""

        return prompt

    def run(self, content, grade):
        prompt = self.build_prompt(content, grade)

        for i in range(self.retries):
            print(f"[REVIEW] try {i+1}/{self.retries}")

            res = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.1
            )

            out = res.choices[0].message.content.strip()
            print("raw:\n", out, "\n")

            try:
                data = extract_json(out)
                return validate_reviewer(data)

            except Exception as err:
                print("error:", err)

                prompt = f"""
Fix this.

Error:
{err}

Previous output:
{out}

Return ONLY valid JSON with:
status and feedback.
"""

        raise Exception("review failed")