import gradio as gr
<<<<<<< HEAD
from blocks.interface import interface

def main():
    with gr.Blocks() as app:
        interface()
=======
from blocks.Interface import interface

def main():
    with gr.Blocks() as app:
        interface.create()
>>>>>>> 16c288ee43552c7930c48ef4882389f9e2ac4202

    app.launch()

if __name__ == '__main__':
    main()