import gradio as gr

def left_panel():
    with gr.Blocks(theme="soft") as block:
        gr.Markdown("### 🧭 任务导航")

        with gr.Accordion("📝 代码生成", open=False):
            with gr.Column(variant="panel"):
                gr.Button("从描述生成")
                gr.Button("代码补全")
        
        with gr.Accordion("🔍 代码解释", open=False):
            with gr.Column(variant="panel"):
                gr.Button("生成代码说明文档")
                gr.Button("生成代码注释")

        with gr.Accordion("⚡ 代码增强", open=False):
            with gr.Column(variant="panel"):
                gr.Button("错误修复")
                gr.Button("代码优化")

        with gr.Accordion("✅ 代码测试", open=False):
            with gr.Column(variant="panel"):
                gr.Button("测试用例生成及在线测试")
        
        with gr.Row(variant="compact"):
            gr.Button("⚙️ 设置", size="md")
    
    return block