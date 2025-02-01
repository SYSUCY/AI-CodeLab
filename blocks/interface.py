import gradio as gr

from blocks.toolbox.code_generation import GenerateFromDescription, CodeCompletion
from blocks.toolbox.code_explanation import GenerateCodeDocumentation, GenerateCodeComments
from blocks.toolbox.code_enhancement import BugFixing, CodeOptimization
from blocks.toolbox.code_testing import TestCaseGeneration
# from blocks.toolbox import *

def interface():
    with gr.Blocks() as block:
        mode = gr.State("generate_from_description") # 初始状态为第一个功能

        with gr.Row():
            with gr.Column(scale=1, min_width=245, variant="compact"):
                # left panel (navigation bar)
                with gr.Blocks(theme="soft") as block:
                    gr.Markdown("### 🧭 功能导航")

                    with gr.Accordion("📝 代码生成", open=False):  # code generation
                        with gr.Column(variant="panel"):
                            btn1 = gr.Button("从描述生成")  # generate_from_description
                            btn2 = gr.Button("代码补全")  # code_completion

                            btn1.click(fn=lambda: "generate_from_description", outputs=[mode])
                            btn2.click(fn=lambda: "code_completion", outputs=[mode])

                    with gr.Accordion("🔍 代码解释", open=False):  # code explanation
                        with gr.Column(variant="panel"):
                            btn3 = gr.Button("生成代码说明")  # generate_code_documentation
                            btn4 = gr.Button("生成代码注释")  # generate_code_comments

                            btn3.click(fn=lambda: "generate_code_documentation", outputs=[mode])
                            btn4.click(fn=lambda: "generate_code_comments", outputs=[mode])

                    with gr.Accordion("⚡ 代码增强", open=False):  # code enhancement
                        with gr.Column(variant="panel"):
                            btn5 = gr.Button("错误修复")  # bug_fixing
                            btn6 = gr.Button("代码优化")  # code_optimization

                            btn5.click(fn=lambda: "bug_fixing", outputs=[mode])
                            btn6.click(fn=lambda: "code_optimization", outputs=[mode])

                    with gr.Accordion("✅ 代码测试", open=False):  # code testing
                        with gr.Column(variant="panel"):
                            btn7 = gr.Button("测试用例生成及在线测试")  # test_case_generation

                            btn7.click(fn=lambda: "test_case_generation", outputs=[mode])

                    with gr.Row(variant="compact"):
                        btn_config = gr.Button("⚙️ 设置", size="md")

            with gr.Column(scale=9, min_width=800):
                # code editor
                with gr.Blocks() as block:
                    gr.Code()
        with gr.Row():
            # toolbox
            with gr.Column():
                gr.Markdown("### 🔧 功能区")

                @gr.render(inputs=mode)
                def render_toolbox(mode):
                    if mode == "generate_from_description":
                        GenerateFromDescription.get_block()
                    elif mode == "code_completion":
                        CodeCompletion.get_block()
                    elif mode == "generate_code_documentation":
                        GenerateCodeDocumentation.get_block()
                    elif mode == "generate_code_comments":
                        GenerateCodeComments.get_block()
                    elif mode == "bug_fixing":
                        BugFixing.get_block()
                    elif mode == "code_optimization":
                        CodeOptimization.get_block()
                    elif mode == "test_case_generation":
                        TestCaseGeneration.get_block()
