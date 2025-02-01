import gradio as gr
from blocks.interface import interface

def main():
    with gr.Blocks() as app:
        interface()

    app.launch()

if __name__ == '__main__':
    main()