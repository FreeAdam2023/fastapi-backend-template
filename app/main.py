from fastapi import FastAPI, Request
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.api.v1.api import router as api_v1_router
from app.exceptions.handlers import register_exception_handlers
from app.middleware.language import LanguageMiddleware
from app.middleware.trace_and_exception import TraceIDExceptionMiddleware
from app.models import get_all_document_models
from app.core.config import settings
from app.core.init_indexes import ensure_user_indexes  # ✅ 引入索引初始化函数

app = FastAPI()

# 注册路由
app.include_router(api_v1_router, prefix="/api/v1")

# 注册异常处理
register_exception_handlers(app)

# 注册中间件（注意顺序）
app.add_middleware(LanguageMiddleware)
app.add_middleware(TraceIDExceptionMiddleware)


@app.on_event("startup")
async def startup_event():
    # 初始化 MongoDB 客户端
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]

    # 初始化 Beanie 文档模型
    document_models = get_all_document_models()
    await init_beanie(database=db, document_models=document_models)

    # ✅ 调用统一的索引初始化逻辑
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
