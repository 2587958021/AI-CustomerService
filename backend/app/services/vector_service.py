import chromadb
from app.core.config import get_settings
from app.services.llm_service import llm_service

settings = get_settings()

class VectorService:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_PATH)
        self.collection = self.client.get_or_create_collection("knowledge_base")
    
    def add_document(self, doc_id: str, chunks: list):
        """添加文档到向量库"""
        ids = []
        documents = []
        embeddings = []
        metadatas = []
        
        for i, chunk in enumerate(chunks):
            chunk_id = f"{doc_id}_chunk_{i}"
            embedding = llm_service.get_embedding(chunk)
            
            ids.append(chunk_id)
            documents.append(chunk)
            embeddings.append(embedding)
            metadatas.append({"doc_id": doc_id, "chunk_index": i})
        
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
    
    def search(self, query: str, top_k: int = 3) -> list:
        """搜索相关知识"""
        query_embedding = llm_service.get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        chunks = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            chunks.append({
                "content": doc,
                "doc_id": metadata["doc_id"]
            })
        
        return chunks
    
    def delete_document(self, doc_id: str):
        """删除文档"""
        self.collection.delete(where={"doc_id": doc_id})

vector_service = VectorService()
