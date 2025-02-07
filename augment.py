def generate_prompt(task, language, code):
    prompts = {
        "错误修复": f"""
            请分析以下 {language} 代码中的错误，并给出修复建议。
            代码：
            ```{language}
            {code}
            ```
            按以下格式响应：
            1. 错误类型：[错误类型]
               位置：[行号]
               建议修复：[修改后的代码片段]
            """,
        "代码优化": f"""
            请优化以下 {language} 代码的性能和可读性。
            代码：
            ```{language}
            {code}
            ```
            按以下格式响应：
            1. 优化点：[优化描述]
               修改后代码：[代码片段]
               预期改进：[性能/可读性提升说明]
            """
    }
    return prompts[task]

