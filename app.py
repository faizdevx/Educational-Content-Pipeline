import gradio as gr
from generator_agent import GeneratorAgent
from reviewer_agent import ReviewerAgent

gen = GeneratorAgent()
rev = ReviewerAgent()


def run_pipeline(grade, topic):
    # quick sanity check
    if not str(grade).strip() or not topic.strip():
        return {}, "enter grade + topic", [], {}

    logs = []

    # step 1 - generate
    logs.append("step 1: generator...")
    try:
        out = gen.run(grade, topic)
        logs.append("ok\n")
    except Exception as e:
        logs.append(f"generator broke: {e}")
        return {}, "\n".join(logs), [], {}

    # step 2 - review
    logs.append("step 2: reviewer...")
    try:
        review = rev.run(out, grade)
        logs.append(f"status: {review['status']}\n")
    except Exception as e:
        logs.append(f"review failed: {e}")
        return out, "\n".join(logs), [], {}

    refined = {}

    # step 3 - optional refine
    if review["status"] == "fail":
        logs.append("step 3: retry with feedback...")
        try:
            refined = gen.run(grade, topic, feedback=review["feedback"])
            logs.append("refined ok")
        except Exception as e:
            logs.append(f"refine failed: {e}")
            refined = {"error": str(e)}
    else:
        logs.append("step 3 skipped")

    return out, "\n".join(logs), review["feedback"], refined


# UI

with gr.Blocks() as app:

    gr.Markdown("# AI Content Pipeline")

    with gr.Row():
        grade_in = gr.Textbox(label="Grade", placeholder="4")
        topic_in = gr.Textbox(label="Topic", placeholder="Angles")

    run_btn = gr.Button("Run")

    log_box = gr.Textbox(label="log", lines=6)

    gr.Markdown("### generator output")
    out_box = gr.JSON()

    gr.Markdown("### feedback")
    fb_box = gr.JSON()

    gr.Markdown("### refined (if failed)")
    ref_box = gr.JSON()

    run_btn.click(
        fn=run_pipeline,
        inputs=[grade_in, topic_in],
        outputs=[out_box, log_box, fb_box, ref_box]
    )


if __name__ == "__main__":
    app.launch()