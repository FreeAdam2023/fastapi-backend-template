"""
@Time ：2025-04-05
@Auth ：Adam Lyu
@Desc ：全局异常捕获 + trace_id 注入中间件
"""

import uuid
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class TraceIDExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id

        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f"[{trace_id}] Unhandled exception: {repr(exc)}", exc_info=True)

            return JSONResponse(
                status_code=500,
                content={
                    "error": {
                        "code": "INTERNAL_SERVER_ERROR",
                        "message": "服务器异常，请稍后重试",
                        "trace_id": trace_id
                    }
                }
            )
