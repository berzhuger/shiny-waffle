from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="forbid",
    )

    #infra
    postgres_url: str = Field(default="postgresql://techflow:dev_only@localhost:5432/techflow")
    qdrant_url: str = Field(default="http://localhost:6333")
    redis_url: str = Field(default="redis://localhost:6379")

    #LLM providers
    anthropic_api_key: SecretStr 
    openai_api_key: SecretStr | None = None
    cohere_api_key: SecretStr | None = None

    environment: str = Field(default="dev")
    log_level: str = Field(default="INFO")
    embedder_model: str = Field(default="text-embedding-3-small")
    chunk_size: int = Field(default=512, ge=128, le=2048)
    chunk_overlap: int = Field(default=50, ge=0, le=200)

settings = Settings()

