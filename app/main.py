"""
@Time  ：2025-04-07
@Auth  ：Adam Lyu
"""

from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.api.v1.api import router as api_v1_router
from app.exceptions.handlers import register_exception_handlers
from app.middleware.auth import AuthMiddleware
from app.middleware.language import LanguageMiddleware
from app.middleware.trace_and_exception import TraceIDExceptionMiddleware
from app.models import get_all_document_models
from app.core.config import settings
from app.core.init_indexes import ensure_user_indexes


def create_app() -> FastAPI:
    app = FastAPI()

    # 注册中间件（注意顺序）
    app.add_middleware(LanguageMiddleware)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(TraceIDExceptionMiddleware)

    # 注册路由
    app.include_router(api_v1_router, prefix="/api/v1")

    # 注册异常处理
    register_exception_handlers(app)

    return app


# ✅ 创建正式应用（本地运行或部署时用到）
app = create_app()


@app.on_event("startup")
async def startup_event():
    # 初始化 MongoDB 客户端
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]

    # 初始化 Beanie 文档模型
    await init_beanie(database=db, document_models=get_all_document_models())

    # 初始化索引
    await ensure_user_indexes()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/test")
async def test_lang(request: Request):
    _ = request.state._
    return {"message": _("Hello!")}
