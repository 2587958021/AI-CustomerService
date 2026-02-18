from zhipuai import ZhipuAI
from app.core.config import get_settings
import numpy as np

settings = get_settings()

class LLMService:
    def __init__(self):
        self.client = ZhipuAI(api_key=settings.ZHIPU_API_KEY)
        self.model = settings.LLM_MODEL
        self.embedding_model = settings.EMBEDDING_MODEL
    
    def get_embedding(self, text: str) -> list:
        """获取文本向量"""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def chat(self, messages: list, context: str = "") -> str:
        """对话生成"""
        system_prompt = """你是一个专业的智能客服助手。请根据提供的知识库内容回答用户问题。
如果知识库中没有相关信息，请礼貌地告知用户你无法回答这个问题。
请保持回答简洁、专业、有帮助。"""
        
        if context:
            system_prompt += f"\n\n参考知识库内容：\n{context}"
        
        full_messages = [{"role": "system", "content": system_prompt}] + messages
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content

llm_service = LLMService()
