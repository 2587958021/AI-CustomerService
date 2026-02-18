# AI 智能客服系统 - 产品需求文档

## 项目概述

基于 RAG（检索增强生成）技术的智能客服问答系统，能够根据知识库内容回答用户问题，提供 7x24 小时智能客服服务。

## 核心功能

### 1. 知识库管理
- 上传文档（PDF、Word、TXT）
- 自动文档解析和分段
- 向量化存储到 ChromaDB
- 知识库增删改查

### 2. 智能问答
- 用户输入问题
- RAG 检索相关知识
- LLM 生成回答
- 显示引用来源

### 3. 对话管理
- 多轮对话支持
- 对话历史保存
- 上下文理解

### 4. 管理后台
- 知识库管理界面
- 问答记录查看
- 系统配置

## 技术栈

- **前端**: Vue 3 + Vite + Element Plus
- **后端**: Python + FastAPI
- **向量数据库**: ChromaDB
- **LLM**: 智谱 AI GLM-4-Flash
- **文档解析**: PyPDF2、python-docx
- **向量嵌入**: 智谱 AI Embedding API

## 页面结构

### 用户端
1. **首页** - 系统介绍
2. **对话页面** - 聊天界面
3. **历史记录** - 查看历史对话

### 管理端
1. **知识库管理** - 上传/删除文档
2. **问答记录** - 查看所有对话
3. **系统设置** - API 配置等

## 数据结构

### 知识库文档
```json
{
  "id": "doc_001",
  "title": "产品使用手册",
  "content": "文档内容...",
  "chunks": [
    {"id": "chunk_001", "content": "分段内容", "embedding": [...]}
  ],
  "createdAt": "2025-02-18",
  "updatedAt": "2025-02-18"
}
```

### 对话记录
```json
{
  "id": "chat_001",
  "messages": [
    {"role": "user", "content": "问题"},
    {"role": "assistant", "content": "回答", "sources": ["chunk_001"]}
  ],
  "createdAt": "2025-02-18"
}
```

## API 接口

### 知识库
- `POST /api/documents` - 上传文档
- `GET /api/documents` - 获取文档列表
- `DELETE /api/documents/{id}` - 删除文档

### 问答
- `POST /api/chat` - 发送消息
- `GET /api/chat/history` - 获取历史记录
- `DELETE /api/chat/{id}` - 删除对话

## 开发计划

1. **Day 1**: 搭建项目结构，实现文档上传和解析
2. **Day 2**: 实现向量化和 ChromaDB 存储
3. **Day 3**: 实现 RAG 检索和问答接口
4. **Day 4**: 开发前端界面
5. **Day 5**: 集成测试和部署

## 项目信息

- **开发者**: 吴叶龙
- **邮箱**: w2587913928@163.com
- **开发时间**: 2025年2月
