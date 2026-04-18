import json
import re


def extract_json(text):
    # try to clean common markdown junk
    text = text.replace("```json", "").replace("```", "")

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("no json found")

    chunk = text[start:end + 1]

    try:
        return json.loads(chunk)
    except json.JSONDecodeError:
        # quick fixes for common LLM mistakes
        chunk = re.sub(r",\s*}", "}", chunk)
        chunk = re.sub(r",\s*]", "]", chunk)
        return json.loads(chunk)


def validate_generator(data):
    # explanation check
    exp = data.get("explanation")
    if not isinstance(exp, str) or not exp.strip():
        raise ValueError("invalid explanation")

    mcqs = data.get("mcqs")
    if not isinstance(mcqs, list) or not mcqs:
        raise ValueError("mcqs missing or empty")

    for i, m in enumerate(mcqs):
        q = m.get("question")
        if not isinstance(q, str) or not q.strip():
            raise ValueError(f"bad question at {i}")

        opts = m.get("options")
        if not isinstance(opts, list) or len(opts) != 4:
            raise ValueError(f"mcq {i}: need 4 options")

        for j, o in enumerate(opts):
            if not isinstance(o, str) or not o.strip():
                raise ValueError(f"mcq {i}, opt {j} invalid")

        ans = m.get("answer")
        if ans not in opts:
            raise ValueError(f"mcq {i}: answer not in options")

    return data


def validate_reviewer(data):
    status = data.get("status")

    if status not in ["pass", "fail"]:
        raise ValueError("status must be pass or fail")

    fb = data.get("feedback")

    if not isinstance(fb, list):
        raise ValueError("feedback must be list")

    if status == "fail" and len(fb) == 0:
        raise ValueError("fail but no feedback")

    return data