from libs.install_lib import is_package_installed, install_package

if not is_package_installed("gradio_codeextend"):
    install_package("./libs/gradio_codeextend-0.0.1-py3-none-any.whl")

import gradio as gr
from blocks.Interface import interface
from core.code_execution.setup_docker import setup_docker


def main():
    setup_docker()

    with gr.Blocks() as app:
        interface.create()

    app.launch()

if __name__ == '__main__':
    main()