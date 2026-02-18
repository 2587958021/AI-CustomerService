from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # API Keys
    ZHIPU_API_KEY: str = ""
    
    # ChromaDB
    CHROMA_DB_PATH: str = "./chroma_db"
    
    # Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # LLM
    LLM_MODEL: str = "glm-4-flash"
    EMBEDDING_MODEL: str = "embedding-3"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
