from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    # Server
    env: str = Field(default="development")

    # Vector DB
    chroma_dir: str = Field(default="./data/chroma", env="CHROMA_DIR")

    # AI keys and models
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    perplexity_api_key: Optional[str] = Field(default=None, env="PERPLEXITY_API_KEY")
    sentence_transformer_model: str = Field(default="all-MiniLM-L6-v2")

    # RAG parameters
    chunk_tokens: int = 700
    chunk_overlap: int = 80

    postgres_host: str = Field(..., env="POSTGRES_HOST")
    postgres_port: int = Field(..., env="POSTGRES_PORT")
    postgres_db: str = Field(..., env="POSTGRES_DB")
    postgres_user: str = Field(..., env="POSTGRES_USER")
    postgres_password: str = Field(..., env="POSTGRES_PASSWORD")
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    cursor_api_key: str = Field(..., env="CURSOR_API_KEY")


    class Config:
        extra = "ignore"
        case_sensitive = False
        env_file = ".env"


settings = Settings()  # Singleton-style access


