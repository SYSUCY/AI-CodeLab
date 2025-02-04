import gradio as gr
from blocks.Interface import interface

def main():
    with gr.Blocks() as app:
        interface.create()

    app.launch()

if __name__ == '__main__':
    main()