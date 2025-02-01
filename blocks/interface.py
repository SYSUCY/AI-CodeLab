import gradio as gr

from blocks.toolbox.code_generation import GenerateFromDescription, CodeCompletion
from blocks.toolbox.code_explanation import GenerateCodeDocumentation, GenerateCodeComments
from blocks.toolbox.code_enhancement import BugFixing, CodeOptimization
from blocks.toolbox.code_testing import TestCaseGeneration
# from blocks.toolbox import *

NAV_ITEMS = {
    "📝 代码生成": ["从描述生成", "代码补全"],
    "🔍 代码解释": ["生成代码说明", "生成代码注释"],
    "⚡ 代码增强": ["错误修复", "代码优化"],
    "✅ 代码测试": ["测试用例生成及在线测试"]
}

def interface():
    with gr.Blocks() as block:
        mode = gr.State("None") # 初始状态

        with gr.Row():
            with gr.Column(scale=1, min_width=245, variant="compact"):
                # left panel (navigation bar)
                gr.Markdown("### 🧭 功能导航")

                radio_components = []

                for category, items in NAV_ITEMS.items():
                    radio = gr.Radio(
                        choices=items,
                        label=category,
                    )
                    radio_components.append(radio)

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
                    print(mode)
                    if mode == "从描述生成":
                        GenerateFromDescription.get_block()
                    elif mode == "代码补全":
                        CodeCompletion.get_block()
                    elif mode == "生成代码说明":
                        GenerateCodeDocumentation.get_block()
                    elif mode == "生成代码注释":
                        GenerateCodeComments.get_block()
                    elif mode == "错误修复":
                        BugFixing.get_block()
                    elif mode == "代码优化":
                        CodeOptimization.get_block()
                    elif mode == "测试用例生成及在线测试":
                        TestCaseGeneration.get_block()

        for radio in radio_components:
            radio.select(
                fn=handle_nav_selection_for_radios,
                inputs=radio,
                outputs=radio_components,
            )
            radio.select(
                fn=lambda x: x,
                inputs=radio,
                outputs=mode,
            )

def handle_nav_selection_for_radios(selected_item): # 导航栏按钮选中事件的handler
    """处理导航选择事件：选中一个时自动取消其他分类的选择"""
    radio_components_update = []

    for item in NAV_ITEMS.items():
        if selected_item in item[1]:
            radio_components_update.append(gr.update(value=selected_item))
        else:
            radio_components_update.append(None)


    return radio_components_update
