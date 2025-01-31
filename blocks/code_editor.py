import gradio as gr

def code_editor():
    with gr.Blocks() as block:
        gr.Code()
    
    return block