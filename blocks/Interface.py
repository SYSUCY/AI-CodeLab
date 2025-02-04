import gradio as gr
from chat import ChatUI

class Interface:
    def __init__(self):
        self._nav_items = {
            "📝 代码生成": ["从描述生成", "代码补全"],
            "🔍 代码解释": ["生成代码说明", "生成代码注释"],
            "⚡ 代码增强": ["错误修复", "代码优化"],
            "✅ 代码测试": ["测试用例生成"]
        }
        # 下面包含了Gradio中Code组件支持的所有语言
        self._lang_map = {
            # 通用编程语言
            'Python': 'python',
            'C': 'c',
            'C++': 'cpp',
            'R': 'r',

            # 标记语言/数据格式
            'Markdown': 'markdown',
            'JSON': 'json',
            'HTML': 'html',
            'CSS': 'css',
            'YAML': 'yaml',
            'Dockerfile': 'dockerfile',

            # 脚本语言
            'JavaScript': 'javascript',
            'TypeScript': 'typescript',
            'Shell': 'shell',
            'Jinja2': 'jinja2',

            # SQL及其方言
            'SQL': 'sql',
            'Microsoft SQL': 'sql-msSQL',
            'MySQL': 'sql-mySQL',
            'MariaDB': 'sql-mariaDB',
            'SQLite': 'sql-sqlite',
            'Cassandra Query Language (CQL)': 'sql-cassandra',
            'PL/SQL': 'sql-plSQL',
            'HiveQL': 'sql-hive',
            'PL/pgSQL': 'sql-pgSQL',
            'GraphQL': 'sql-gql',
            'Greenplum SQL': 'sql-gpSQL',
            'Spark SQL': 'sql-sparkSQL',
            'Esper EPL': 'sql-esper'
        }
        self._model_list = [
            "DeepSeek-R1-Distill-Qwen-32B",
            "qwen-max",
            "qwen-plus",
            "qwen-turbo",
        ]

        # 控件
        self.btn_config = None
        self.btn_upload = None
        self.lang_selector = None
        self.model_selector = None
        self.editor = None
        self.nav_radio_components = []  # 左侧导航栏的所有radio控件

        # 存储当前界面状态
        self.selected_feature = ""
        self.selected_language = ""
        self.selected_model = ""

    #---------------- 公有接口-----------------#
    def create(self):
        with gr.Blocks() as block:
            with gr.Row():
                with gr.Column(scale=1, min_width=245, variant="compact"):
                    # left panel (navigation bar)
                    gr.Markdown("### 🧭 功能导航")

                    self.nav_radio_components = []

                    for category, items in self._nav_items.items():
                        radio = gr.Radio(
                            choices=items,
                            label=category,
                        )
                        self.nav_radio_components.append(radio)

                    self.btn_config = gr.Button("⚙️ 设置", size="md")

                    self.btn_upload = gr.Button("上传代码文件", variant="primary", size="md")

                with gr.Column(scale=9, min_width=800):
                    with gr.Row():
                        self.lang_selector = gr.Dropdown(label="请选择编程语言", choices=list(self._lang_map.keys()),
                                                    interactive=True, filterable=True, value=None)
                        self.model_selector = gr.Dropdown(label="请选择使用的模型", choices=self._model_list,
                                                          interactive=True, filterable=True, value=None)
                    # code editor
                    self.editor = gr.Code(lines=30, max_lines=30, interactive=True)
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

            model_selector = self.get_model()
            lang_selector = self.get_language()
            btn_code_generate.click(
                fn=self.handle_generate_code,
                inputs=[user_input_box, code_input_box, model_selector, lang_selector],
                outputs=[output_code_box]
            )
            #test

            for radio in self.nav_radio_components:
                radio.select(
                    fn=self._handle_nav_selection,
                    inputs=radio,
                    outputs=self.nav_radio_components,
                )

            self.lang_selector.change(
                fn=self._handle_lang_selection,
                inputs=self.lang_selector,
                outputs=self.editor,
            )

            self.model_selector.change(
                fn=self._handle_model_selection,
                inputs=self.model_selector,
            )

    def get_feature(self) -> str:
        """
        获取用户当前在左侧导航栏选择的功能名称（与界面上的文本相同，是中文）。

        Returns:
            str: 当前选择的功能名称。
            未选择功能时，返回空字符串。
        """
        return self.selected_feature

    def get_language(self) -> str:
        """
        获取用户当前选择的编程语言名称（与界面上的文本相同）。

        Returns:
            str: 当前选择的编程语言名称。
            未选择编程语言时，返回空字符串。
        """
        return self.selected_language

    def get_model(self) -> str:
        """
        获取用户当前选择的模型名称（与界面上的文本相同）。

        Returns:
            str: 当前选择的模型名称。
            未选择模型时，返回空字符串。
        """
        return self.selected_model

    # ----------------私有方法-----------------#
    def _handle_nav_selection(self, selected_item: str):  # 导航栏按钮选中事件的handler
        """处理导航选择事件：选中一个时自动取消其他分类的选择"""
        self.selected_feature = selected_item

        radio_components_update = []

        for item in self._nav_items.items():
            if selected_item in item[1]:
                radio_components_update.append(gr.update(value=selected_item))
            else:
                radio_components_update.append(None)

        return radio_components_update

    def _handle_lang_selection(self, selected_item: str):
        self.selected_language = selected_item

        return gr.update(language=self._lang_map[selected_item])

    def _handle_model_selection(self, selected_item: str):
        self.selected_model = selected_item

interface = Interface()