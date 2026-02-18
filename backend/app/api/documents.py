from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_service import document_service
from app.services.vector_service import vector_service
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """上传文档"""
    try:
        # 保存文件
        file_path = document_service.save_file(file)
        
        # 解析文档
        text = document_service.parse_document(file_path)
        
        # 分块
        chunks = document_service.chunk_text(text)
        
        # 生成文档ID
        doc_id = str(uuid.uuid4())
        
        # 添加到向量库
        vector_service.add_document(doc_id, chunks)
        
        return {
            "success": True,
            "doc_id": doc_id,
            "filename": file.filename,
            "chunks_count": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_documents():
    """获取文档列表"""
    # 简化版本，实际应该从数据库查询
    return {"documents": []}

@router.delete("/{doc_id}")
async def delete_document(doc_id: str):
    """删除文档"""
    try:
        vector_service.delete_document(doc_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
