import gradio as gr
from chat import ChatUI
import os

chat_ui = ChatUI()
method = '从描述生成'

NAV_ITEMS = {
    "📝 代码生成": ["从描述生成", "代码补全"],
    "🔍 代码解释": ["生成代码说明", "生成代码注释"],
    "⚡ 代码增强": ["错误修复", "代码优化"],
    "✅ 代码测试": ["测试用例生成"]
}

def interface():
    with gr.Blocks() as block:
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

                btn_upload = gr.Button("上传代码文件", variant="primary", size="md")

                btn_download = gr.Button("下载代码文件", variant="primary", size="md")

            with gr.Column(scale=9, min_width=800):
                with gr.Row():
                    lang_selector = gr.Dropdown(label="请选择编程语言",
                                                choices=["Python", "Java", "C++", "C#", "JavaScript", "TypeScript"])
                    model_selector = gr.Dropdown(label="请选择使用的模型",
                                                 choices=["DeepSeek-R1-Distill-Qwen-32B"])
                # code editor
                gr.Code(lines=30)
        with gr.Row():
            # toolbox
            with gr.Column():
                gr.Markdown("### 🔧 功能区")
        with gr.Row():
            with gr.Column(scale=9, min_width=800):
                with gr.Row():
                    user_input_box = gr.Textbox("", label="📄 输入区", lines=25)
                    code_input_box = gr.Code(lines=30)
                with gr.Row():
                    btn_code_generate = gr.Button("生成代码", variant="primary", size="md")
                with gr.Row():
                    output_code_box = gr.Code(lines=10)

        btn_code_generate.click(
            fn=handle_generate_code,
            inputs=[user_input_box, code_input_box, model_selector, lang_selector],
            outputs=[output_code_box]
        )



        for radio in radio_components:
            radio.select(
                fn=handle_nav_selection,
                inputs=radio,
                outputs=radio_components,
            )


def handle_nav_selection(selected_item): # 导航栏按钮选中事件的handler
    """处理导航选择事件：选中一个时自动取消其他分类的选择"""
    radio_components_update = []

    for item in NAV_ITEMS.items():
        if selected_item in item[1]:
            radio_components_update.append(gr.update(value=selected_item))
            method = selected_item
        else:
            radio_components_update.append(None)


    return radio_components_update


# def handle_generate_code(user_input, code_input, model_selection="DeepSeek-R1-Distill-Qwen-32B"):
#     """
#     处理生成代码按钮的点击事件，根据导航栏选择不同的生成逻辑
#     :param user_input: Textbox 中的用户输入的自然语言描述
#     :param code_input: Code 中的待补全代码
#     :param model_selection: 选择的模型
#     :return: 生成的代码
#     """
#     input_text = ""
#     code_to_generate = ""
#     # 如果选择的是从描述生成，直接用自然语言生成代码
#     if method == "从描述生成":
#         input_text = user_input  # 直接使用自然语言输入
#         code_to_generate = ""
#
#     # 如果选择的是代码补全，根据输入的代码和描述生成补全代码
#     elif method == "代码补全":
#         input_text = user_input  # 使用自然语言描述
#         code_to_generate = code_input  # 使用待补全的代码
#
#     # 调用 ChatUI 进行流式生成
#     response = ""
#     for chunk in chat_ui.gradio_interface(model_selection, input_text + "\n" + code_to_generate):
#         response += chunk  # 累加生成的代码
#
#     return response

def handle_generate_code(user_input, code_input, model_selection="DeepSeek-R1-Distill-Qwen-32B", lang_selection="Python"):
    """
    处理生成代码按钮的点击事件，根据导航栏选择不同的生成逻辑
    :param user_input: Textbox 中的用户输入的自然语言描述
    :param code_input: Code 中的待补全代码
    :param model_selection: 选择的模型
    :return: 生成的代码
    """
    prompt = ""

    if method == "从描述生成":
        prompt = f"以下是自然语言描述:\n" \
                 f"{user_input}\n" \
                 f"根据上述描述，生成相应的{lang_selection}代码，并且使用特定的标记包裹代码部分。\n" \
                 f"请确保代码被标记为代码块，并且其外部标记如下:\n" \
                 f"<code> ... </code>"

    elif method == "代码补全":
        prompt = f"以下是自然语言描述:\n" \
                 f"{user_input}\n" \
                 f"以下是待补全的代码:\n" \
                 f"{code_input}\n" \
                 f"根据上述描述和待补全的代码，生成完整的{lang_selection}代码，并且使用特定的标记包裹代码部分。\n" \
                 f"请确保代码被标记为代码块，并且其外部标记如下:\n" \
                 f"<code> ... </code>"

    # 调用 ChatUI 进行流式生成
    response = ""
    for chunk in chat_ui.gradio_interface(model_selection, prompt):
        response += chunk  # 累加生成的代码

    # 提取 <code> 和 </code> 标签之间的部分作为最终返回值
    start_index = response.find("<code>") + len("<code>")
    end_index = response.find("</code>", start_index)

    # 如果找到了 <code> 和 </code>，返回其中的内容
    if start_index != -1 and end_index != -1:
        final_code = response[start_index:end_index]
    else:
        final_code = response  # 如果没有找到，返回原始响应（可能需要处理错误情况）

    return final_code

