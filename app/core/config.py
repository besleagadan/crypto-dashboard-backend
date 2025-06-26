from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # PostgreSQL
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # Mongodb
    MONGO_URL: str
    MONGO_DB_NAME: str

    # Redis
    REDIS_BROKER_URL: str
    REDIS_BACKEND_URL: str

    # Binance
    BINANCE_WS_URL: str

    # Google
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

# Create a singleton settings instance
settings = Settings()
