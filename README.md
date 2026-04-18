# 📚 AI Educational Content Pipeline

This project is a simple but structured attempt to build an AI system that doesn’t just generate content, but also evaluates it.

Instead of relying on a single model output, the idea is to introduce a second step where the generated content is reviewed and, if needed, improved.

---

## 🚀 What this project does

The pipeline works in three steps:

1. A **Generator Agent** creates educational content based on a given grade and topic
2. A **Reviewer Agent** checks if the content is correct, clear, and appropriate
3. If the reviewer finds issues, the system can regenerate the content with feedback

So instead of:

```text
Prompt → Output
```

we move to:

```text
Prompt → Generate → Review → (Improve if needed)
```

---

## 🧠 Why I built this

Most AI projects stop at generating output.
But in real-world systems, that’s not enough.

Models:

* make formatting mistakes
* give shallow explanations
* hallucinate structure

This project is an attempt to handle those issues using:

* validation
* retries
* feedback loops

---

## 🏗️ How it works

```text
User Input (Grade + Topic)
        ↓
Generator Agent
        ↓
JSON Parsing + Validation
        ↓
Reviewer Agent
        ↓
Pass → Show Output
Fail → Regenerate with feedback
```

---

## 📁 Project Structure

```text
assignment/
│
├── app.py               # Gradio UI
├── generator_agent.py  # Generates content
├── reviewer_agent.py   # Reviews content
├── utils.py            # JSON parsing & validation
└── README.md
```

---

## ⚙️ Setup

### 1. Install dependencies

```bash
pip install gradio huggingface_hub
```

### 2. Set up Hugging Face token

```bash
hf auth login
```

or directly in code:

```python
token = "hf_xxxxxxxxx"
```

---

## ▶️ Running the project

```bash
python app.py
```

Then open:

```
http://127.0.0.1:7860
```

---

## 🧪 Example inputs

You can try things like:

* Grade 6 → Water Cycle
* Grade 10 → Photosynthesis
* Grade 12 → Backpropagation in Neural Networks

---

## 🧩 Components

### Generator Agent

* Generates explanation + MCQs
* Follows a strict JSON structure
* Uses retries if output is invalid

---

### Reviewer Agent

* Checks:

  * correctness
  * clarity
  * grade-level appropriateness
* Returns pass/fail + feedback

---

## ⚠️ Limitations

This is not a perfect system.

* JSON can still break sometimes
* Reviewer can be too lenient
* Complex topics may lack depth
* Output quality depends heavily on prompts

---

## 🔮 Future improvements

Some things that can be improved:

* More strict reviewer (scoring instead of pass/fail)
* Multiple refinement steps
* Better prompt control for advanced topics
* Adding external knowledge (RAG)

---

## 🛠️ Tech used

* Python
* Hugging Face Inference API
* Gradio

---

## 🧠 What I learned

This project made one thing very clear:

> Generating output is easy.
> Controlling output is the real problem.

Working with LLMs is less about calling APIs and more about:

* handling failures
* validating structure
* designing feedback loops

---

## 👤 Author

Faizal
CSE (AI) Student

---

## Final note

This is a small project, but it’s built with the mindset of how real AI systems should work.

Not just “generate something”…
but **check it, fix it, and make it reliable.**
