from fastapi import APIRouter
from pydantic import BaseModel
from app.services.llm_service import llm_service
from app.services.vector_service import vector_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: list = []

class ChatResponse(BaseModel):
    answer: str
    sources: list = []

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """对话接口"""
    try:
        # RAG 检索
        relevant_chunks = vector_service.search(request.message, top_k=3)
        
        # 构建上下文
        context = "\n\n".join([chunk["content"] for chunk in relevant_chunks])
        
        # 构建消息
        messages = []
        for msg in request.history[-5:]:  # 只保留最近5轮
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": request.message})
        
        # 生成回答
        answer = llm_service.chat(messages, context)
        
        return ChatResponse(
            answer=answer,
            sources=[chunk["doc_id"] for chunk in relevant_chunks]
        )
    except Exception as e:
        return ChatResponse(
            answer=f"抱歉，系统出现错误：{str(e)}",
            sources=[]
        )
