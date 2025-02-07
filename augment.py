structured_guidelines = {
    "错误修复": {
        "header": "请严格按以下格式分析代码错误",
        "requirements": [
            "没有错误就只描述潜在错误",
            "需使用错误类型标准术语",
            "必须标注具体行号"
        ],
        "example": """
             ### 错误1
             - 类型: 数组越界
             - 位置: 行17
             - 触发条件: 当input_list为空时
             - 错误现象: IndexError: list index out of range
             - 修复方案: 增加长度检查
             - 代码修正:
                 ```python
                 # 原代码
                 return input_list[0]

                 # 修正后
                 return input_list[0] if len(input_list) > 0 else None
                 ```"""
    },
    "代码优化": {
        "header": "请按以下维度提供优化建议",
        "categories": [
            "时间复杂度优化（如O(n²)→O(n)）",
            "空间效率提升（如减少内存占用）",
            "代码可维护性（如拆分复杂函数）",
            "语言特性利用"
        ],
        "example": """
             ### 优化点1
             - 类型: 循环效率优化
             - 位置: 行5-9
             - 原代码:
                 ```python
                 result = []
                 for i in range(10000):
                     result.append(i*2)
                 ```
             - 优化后:
                 ```python
                 result = [i*2 for i in range(10000)]
                 ```"""
    }
}

def generate_prompt(task, language, code):
    template = {
        "错误修复": f"""
            作为资深{language}开发工程师，{structured_guidelines['错误修复']['header']}：

            代码分析要求：
            {chr(10).join(structured_guidelines['错误修复']['requirements'])}

            原始代码：
            ```{language}
            {code}
            ```

            请按此模板响应：
            {structured_guidelines['错误修复']['example']}

            最后请给出：
            ### 完整修复方案
            包含所有修正的完整代码（用```标记）""",

        "代码优化": f"""
            作为{language}性能优化专家，{structured_guidelines['代码优化']['header']}：

            优化维度应包括：
            {chr(10).join(structured_guidelines['代码优化']['categories'])}

            原始代码：
            ```{language}
            {code}
            ```

            参考示例：
            {structured_guidelines['代码优化']['example']}

            最后请给出：
            ### 完整优化代码
            整合所有优化的最终代码（用```标记）"""
    }

    return template[task]