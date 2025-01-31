import gradio as gr

def right_panel():
    with gr.Blocks() as block:
        gr.Markdown("### 🔧 功能栏")
        gr.Textbox() # 占位，待编写

    return block