import os
import time
import gradio as gr
from openai import OpenAI
from typing import Generator, Optional

class ChatClient:
    """聊天客户端类，用于管理不同提供商的API调用"""
    
    def __init__(self):
        self.providers = {
            "gitee": {
                "base_url": "https://ai.gitee.com/v1",
                "headers": {"X-Failover-Enabled": "true", "X-Package": "1910"}
            }, # 支持模型见：https://ai.gitee.com/serverless-api，推荐您通过其使用DeepSeek-R1-Distill-Qwen-32B模型
            "aliyuncs": {
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
            }, # 支持模型见：https://help.aliyun.com/zh/model-studio/getting-started/models，推荐您通过其使用qwen-max模型(质量最高)，qwen-plus(均衡)，qwen-turbo(速度最快)
            "nvidia": {
                # TODO: 需要添加
            }, # 计划提供deepseek-r1 模型
        }

        # 添加默认模型参数配置
        self.model_params = {
            "DeepSeek-R1-Distill-Qwen-32B": {
                "temperature": 0.6,
                "top_p": 0.8,
                "max_tokens": 4096 # 请不要超过4096，否则会报错，这是gitee的限制，很奇怪？
            },
            "qwen-max": {
                "temperature": 0.7,
                "top_p": 0.8,
                "max_tokens": 8192
            },
            "qwen-plus": {
                "temperature": 0.7,
                "top_p": 0.8,
                "max_tokens": 8192
            },
            "qwen-turbo": {
                "temperature": 0.7,
                "top_p": 0.8,
                "max_tokens": 8192
            }
        }


    def create_client(self, provider: str) -> OpenAI:
        """
        根据提供商创建对应的API客户端
        Args:
            provider: 提供商名称 ('gitee', 'aliyuncs')，见上方__init__
        Returns:
            OpenAI: 配置好的API客户端实例

        注意：gitee 和 aliyuncs 的api_key 环境变量是不同的，需要分别设置
        """
        if provider not in self.providers:
            raise ValueError(f"不支持的提供商: {provider}")
            
        provider_config = self.providers[provider]

        # 根据提供商设置api_key 
        if provider == "gitee":
            api_key = os.getenv("GITEE_API_KEY")
        elif provider == "aliyuncs":
            api_key = os.getenv("DASHSCOPE_API_KEY")
        else:
            raise ValueError(f"不支持的提供商: {provider}")
        
        # 添加默认headers
        if "headers" not in provider_config:
            provider_config["headers"] = {}
        
        if api_key is None:
            raise ValueError(f"未设置{provider}的API密钥")
        
        return OpenAI(
            base_url=provider_config["base_url"],
            api_key=api_key,
            default_headers=provider_config["headers"]
        )

    def stream_chat(self, provider: str, model: str, context: list, **kwargs) -> Generator[str, None, None]:
        """
        生成聊天响应的流式输出
        Args:
            provider: 提供商名称
            model: 模型名称
            context: 完整的消息上下文列表，格式为 [{"role": "user", "content": "消息内容"}, ...]
            **kwargs: 其他模型参数，会覆盖默认参数
        Yields:
            str: 响应片段
        """
        if model not in self.model_params:
            raise ValueError(f"不支持的模型: {model}")
        
        client = self.create_client(provider)

        # 检查用户的context是否合法
        for message in context:
            if "role" not in message or "content" not in message:
                raise ValueError("缺少role或content")
            if message["role"] not in ["system", "user", "assistant"]:
                raise ValueError("role必须是system, user或assistant")
            if message["role"] == "system" and "DeepSeek-R1" in model:
                raise ValueError("system message不建议添加到DeepSeek-R1系列模型，包括蒸馏模型") 

        # 获取默认参数并更新自定义参数
        params = self.model_params.get(model, {}).copy()
        params.update(kwargs)
        
        response = client.chat.completions.create(
            model=model,
            messages=context,
            stream=True,
            **params
        )
        for chunk in response:
            data = chunk.model_dump() if hasattr(chunk, "model_dump") else chunk
            if "choices" in data and len(data["choices"]) > 0:
                delta = data["choices"][0].get("delta", {})
                content = delta.get("content")
                if content:
                    # 流式输出
                    yield content

        # 模拟输出（测试用）
        # for i in range(10):
        #     yield f"Chunk {i}"
        #     time.sleep(0.1)


# 这个这是测试界面，方便各位查看使用案例
class ChatUI:
    """聊天界面类，处理UI相关逻辑"""
    
    def __init__(self):
        self.chat_client = ChatClient()
        # 添加模型到提供商的映射
        self.model_provider_map = {
            "DeepSeek-R1-Distill-Qwen-32B": "gitee",
            "qwen-max": "aliyuncs",
            "qwen-plus": "aliyuncs",
            "qwen-turbo": "aliyuncs"
        }

    def gradio_interface(self, model: str, user_input: str) -> Generator[str, None, None]:
        """
        Gradio接口函数，处理用户输入并返回流式响应
        Args:
            model: 选择的模型名称
            user_input: 用户输入的文本
        Returns:
            Generator[str, None, None]: 生成器，用于流式输出响应
        """
        if not user_input.strip():
            raise ValueError("输入不能为空")
        
        # 根据模型自动选择提供商
        provider = self.model_provider_map.get(model)
        if not provider:
            raise ValueError(f"不支持的模型: {model}")
            
        context = [{"role": "user", "content": user_input}]
        response = ""
        for chunk in self.chat_client.stream_chat(provider, model, context):
            response += chunk
            yield response

    def create_interface(self) -> gr.Blocks:
        """
        创建Gradio界面
        """
        with gr.Blocks() as demo:
            model = gr.Dropdown(
                choices=list(self.model_provider_map.keys()),
                label="选择模型",
                value="DeepSeek-R1-Distill-Qwen-32B"
            )
            user_input = gr.Textbox(
                label="用户输入",
                placeholder="在这里输入您的消息..."
            )
            response = gr.Textbox(label="回复")
            submit_btn = gr.Button("发送")

            submit_btn.click(
                fn=self.gradio_interface,
                inputs=[model, user_input],
                outputs=response
            )

        return demo

def main():
    """
    主函数：启动Gradio界面进行测试
    注意：请勿在生产环境中直接暴露API密钥
    """
<<<<<<< HEAD
    os.environ["GITEE_API_KEY"] = "7IZQCLFXGS4RNWRDUZW5L3FKQXJOZRWMEDQS3I1P"
    os.environ["DASHSCOPE_API_KEY"] = "sk-ff05d1133ae047d6bb221b18755984f4"
=======
>>>>>>> 16c288ee43552c7930c48ef4882389f9e2ac4202

    chat_ui = ChatUI()
    demo = chat_ui.create_interface()
    demo.queue()
    demo.launch()

if __name__ == "__main__":
    main()
