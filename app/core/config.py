"""
@Time ： 2025-04-03
@Auth ： Adam Lyu
"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Auto-detect environment: use .env.test for testing
env_file = ".env.test" if os.getenv("ENVIRONMENT") == "test" else ".env"
load_dotenv(dotenv_path=env_file)


class Settings(BaseSettings):
    # 应用基本配置
    ENVIRONMENT: str = "dev"
    APP_NAME: str = os.getenv("APP_NAME", "3DGates")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    # MongoDB 配置（分开读取后组合）
    MONGO_USERNAME: str = os.getenv("MONGO_USERNAME")
    MONGO_PASSWORD: str = os.getenv("MONGO_PASSWORD")
    MONGO_HOST: str = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT: int = int(os.getenv("MONGO_PORT", 27017))
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "3dgates")
    MONGO_AUTH_SOURCE: str = os.getenv("MONGO_AUTH_SOURCE", "admin")
    FRONTEND_URL: str = "https://www.versegates.com"

    @property
    def MONGO_URI(self) -> str:
        return (
            f"mongodb://{self.MONGO_USERNAME}:{self.MONGO_PASSWORD}"
            f"@{self.MONGO_HOST}:{self.MONGO_PORT}/{self.MONGO_DB_NAME}"
            f"?authSource={self.MONGO_AUTH_SOURCE}"
        )

    # JWT 设置
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # SMTP 邮件配置
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", 465))
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS: bool = os.getenv("MAIL_USE_TLS", "False") == "True"
    MAIL_USE_SSL: bool = os.getenv("MAIL_USE_SSL", "True") == "True"
    MAIL_DEFAULT_SENDER: str = os.getenv("MAIL_DEFAULT_SENDER", "noreply@example.com")


# 全局配置实例
settings = Settings()
