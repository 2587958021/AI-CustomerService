from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from datetime import datetime

app = FastAPI(title="AI Customer Service API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据目录
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# 数据文件路径
DOCUMENTS_FILE = os.path.join(DATA_DIR, "documents.json")
KNOWLEDGE_FILE = os.path.join(DATA_DIR, "knowledge.json")
CHAT_HISTORY_FILE = os.path.join(DATA_DIR, "chat_history.json")

# 确保数据文件存在
def init_data_files():
    if not os.path.exists(DOCUMENTS_FILE):
        with open(DOCUMENTS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
    if not os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, 'w', encoding='utf-8') as f:
            json.dump([
                {
                    "id": "1",
                    "keywords": ["功能", "产品", "做什么"],
                    "answer": "我们的AI智能客服系统主要功能包括：\n\n1. **文档智能解析** - 支持PDF、Word、TXT等多种格式文档上传和自动解析\n2. **RAG检索增强** - 基于向量数据库的智能检索，精准定位相关知识\n3. **智能对话** - 支持多轮对话，上下文理解，提供专业准确的回答\n4. **知识库管理** - 便捷的知识库管理界面，支持文档增删改查"
                },
                {
                    "id": "2",
                    "keywords": ["联系", "客服", "电话", "邮箱"],
                    "answer": "您可以通过以下方式联系我们：\n\n- **邮箱**：w2587913928@163.com\n- **开发者**：吴叶龙\n- **项目地址**：https://github.com/2587958021/AI-CustomerService\n\n我们会在24小时内回复您的问题。"
                },
                {
                    "id": "3",
                    "keywords": ["价格", "多少钱", "费用"],
                    "answer": "目前我们的AI智能客服系统提供以下方案：\n\n- **免费版**：基础功能，适合个人和小团队使用\n- **专业版**：更多功能和更高配额，适合中小企业\n- **企业版**：定制化解决方案，适合大型企业\n\n具体价格请咨询我们的销售团队。"
                },
                {
                    "id": "4",
                    "keywords": ["支付", "付款", "方式"],
                    "answer": "我们支持多种支付方式：\n\n- 支付宝\n- 微信支付\n- 银行转账\n- 对公账户\n\n企业用户还可以选择月付或年付，年付可享受8折优惠。"
                },
                {
                    "id": "5",
                    "keywords": ["技术", "技术栈", "原理"],
                    "answer": "我们的系统采用业界领先的技术栈：\n\n**前端**：Vue 3 + Element Plus\n**后端**：FastAPI + Python\n**向量数据库**：ChromaDB\n**大模型**：智谱AI GLM-4\n**文档解析**：PyPDF2、python-docx\n\n基于RAG（检索增强生成）技术，确保回答准确可靠。"
                }
            ], f)
    if not os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

init_data_files()

# 数据模型
class Document(BaseModel):
    id: str
    filename: str
    content: str
    chunks_count: int
    created_at: str

class Knowledge(BaseModel):
    id: str
    keywords: List[str]
    answer: str

class ChatMessage(BaseModel):
    role: str
    content: str
    sources: Optional[List[str]] = None

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = []

# 加载数据
def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# 保存数据
def save_data(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 简单的关键词匹配搜索
def search_knowledge(query: str):
    knowledge = load_data(KNOWLEDGE_FILE)
    query_lower = query.lower()
    
    for item in knowledge:
        for keyword in item["keywords"]:
            if keyword.lower() in query_lower:
                return item["answer"]
    
    return "感谢您的提问！这个问题我需要更多信息才能回答。\n\n您可以尝试询问以下问题：\n- 产品有哪些功能？\n- 如何联系客服？\n- 产品价格是多少？\n- 支持哪些支付方式？\n- 技术栈是什么？"

# ========== 文档 API ==========
@app.get("/api/documents")
async def get_documents():
    """获取所有文档"""
    return load_data(DOCUMENTS_FILE)

@app.post("/api/documents")
async def create_document(doc: Document):
    """添加文档"""
    documents = load_data(DOCUMENTS_FILE)
    documents.append(doc.dict())
    save_data(DOCUMENTS_FILE, documents)
    return doc

@app.delete("/api/documents/{doc_id}")
async def delete_document(doc_id: str):
    """删除文档"""
    documents = load_data(DOCUMENTS_FILE)
    documents = [d for d in documents if d["id"] != doc_id]
    save_data(DOCUMENTS_FILE, documents)
    return {"message": "删除成功"}

# ========== 知识库 API ==========
@app.get("/api/knowledge")
async def get_knowledge():
    """获取所有知识"""
    return load_data(KNOWLEDGE_FILE)

@app.post("/api/knowledge")
async def create_knowledge(knowledge: Knowledge):
    """添加知识"""
    knowledge_list = load_data(KNOWLEDGE_FILE)
    knowledge_list.append(knowledge.dict())
    save_data(KNOWLEDGE_FILE, knowledge_list)
    return knowledge

@app.put("/api/knowledge/{knowledge_id}")
async def update_knowledge(knowledge_id: str, knowledge: Knowledge):
    """更新知识"""
    knowledge_list = load_data(KNOWLEDGE_FILE)
    for i, item in enumerate(knowledge_list):
        if item["id"] == knowledge_id:
            knowledge_list[i] = knowledge.dict()
            save_data(KNOWLEDGE_FILE, knowledge_list)
            return knowledge
    raise HTTPException(status_code=404, detail="知识不存在")

@app.delete("/api/knowledge/{knowledge_id}")
async def delete_knowledge(knowledge_id: str):
    """删除知识"""
    knowledge_list = load_data(KNOWLEDGE_FILE)
    knowledge_list = [k for k in knowledge_list if k["id"] != knowledge_id]
    save_data(KNOWLEDGE_FILE, knowledge_list)
    return {"message": "删除成功"}

# ========== 聊天 API ==========
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """聊天接口"""
    # 搜索知识库
    answer = search_knowledge(request.message)
    
    # 保存聊天记录
    history = load_data(CHAT_HISTORY_FILE)
    history.append({
        "role": "user",
        "content": request.message,
        "timestamp": datetime.now().isoformat()
    })
    history.append({
        "role": "assistant",
        "content": answer,
        "sources": ["知识库"],
        "timestamp": datetime.now().isoformat()
    })
    save_data(CHAT_HISTORY_FILE, history)
    
    return {
        "answer": answer,
        "sources": ["知识库"]
    }

@app.get("/api/chat/history")
async def get_chat_history():
    """获取聊天记录"""
    return load_data(CHAT_HISTORY_FILE)

@app.delete("/api/chat/history")
async def clear_chat_history():
    """清空聊天记录"""
    save_data(CHAT_HISTORY_FILE, [])
    return {"message": "聊天记录已清空"}

# ========== 健康检查 ==========
@app.get("/")
async def root():
    return {"message": "AI Customer Service API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
