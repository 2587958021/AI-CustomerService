# AI 智能客服系统

基于 RAG（检索增强生成）技术的智能客服问答系统。

## 功能特性

- 📄 文档智能解析（PDF、Word、TXT）
- 🔍 RAG 检索增强问答
- 💬 多轮对话支持
- 📚 知识库管理
- 🎨 现代化界面

## 技术栈

- **前端**: Vue 3 + Element Plus
- **后端**: FastAPI + Python
- **向量数据库**: ChromaDB
- **LLM**: 智谱 AI GLM-4

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env 添加 ZHIPU_API_KEY
python -m app.main
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

## 访问

- 前端: http://localhost:3000
- 后端 API: http://localhost:8000

## 开发者

- **姓名**: 吴叶龙
- **邮箱**: w2587913928@163.com
