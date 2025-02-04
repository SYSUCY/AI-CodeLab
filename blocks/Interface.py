import gradio as gr

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

        # 控件
        self.btn_config = None
        self.btn_upload = None
        self.lang_selector = None
        self.model_selector = None
        self.editor = None
        self.nav_radio_components = []  # 左侧导航栏的所有radio控件

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
                        self.model_selector = gr.Dropdown(label="请选择使用的模型")
                    # code editor
                    self.editor = gr.Code(lines=30, max_lines=30, interactive=True)
            with gr.Row():
                # toolbox
                with gr.Column():
                    gr.Markdown("### 🔧 功能区")

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

    def get_feature(self):
        return

    def get_language(self):
        return

    def get_model(self):
        return

    # ----------------私有方法-----------------#
    def _handle_nav_selection(self, selected_item):  # 导航栏按钮选中事件的handler
        """处理导航选择事件：选中一个时自动取消其他分类的选择"""
        radio_components_update = []

        for item in self._nav_items.items():
            if selected_item in item[1]:
                radio_components_update.append(gr.update(value=selected_item))
            else:
                radio_components_update.append(None)

        return radio_components_update

    def _handle_lang_selection(self, selected_item):
        return gr.update(language=self._lang_map[selected_item])

interface = Interface()