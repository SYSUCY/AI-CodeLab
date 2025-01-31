import gradio as gr
from blocks.left_panel import left_panel
from blocks.code_editor import code_editor
from blocks.right_panel import right_panel

def main():
    with gr.Blocks() as app:
        with gr.Row():
            with gr.Column(scale=1, min_width=245, variant="compact"):
                left_panel()
            with gr.Column(scale=9, min_width=800):
                code_editor()
        with gr.Row():
            with gr.Column(min_width=320):
                right_panel()

    app.launch()

if __name__ == '__main__':
    main()