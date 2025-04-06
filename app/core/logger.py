"""
@Time ：2025-04-05
@Auth ：Adam Lyu
@Desc ：通用日志工具，支持 trace_id / user_id / 结构化日志拓展
"""

import logging
import sys
from typing import Optional

class LogHelper:
    def __init__(self, name="3dgates"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] [%(trace_id)s] [%(client_ip)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log(self, level: str, message: str, trace_id: Optional[str] = "-", user_id: Optional[str] = None, **kwargs):
        extra = {"trace_id": trace_id or "-", "client_ip": kwargs.get("client_ip", "-")}
        extra.update(kwargs)  # 包含自定义字段

        full_message = message
        if user_id:
            full_message = f"[user:{user_id}] {message}"

        self.logger.log(getattr(logging, level.upper()), full_message, extra=extra)

    def info(self, message: str, trace_id: Optional[str] = None, user_id: Optional[str] = None, **kwargs):
        self.log("info", message, trace_id, user_id, **kwargs)

    def warning(self, message: str, trace_id: Optional[str] = None, user_id: Optional[str] = None, **kwargs):
        self.log("warning", message, trace_id, user_id, **kwargs)

    def error(self, message: str, trace_id: Optional[str] = None, user_id: Optional[str] = None, **kwargs):
        self.log("error", message, trace_id, user_id, **kwargs)

    def debug(self, message: str, trace_id: Optional[str] = None, user_id: Optional[str] = None, **kwargs):
        self.log("debug", message, trace_id, user_id, **kwargs)


# ✅ 全局日志实例
logger = LogHelper().logger
log = LogHelper()

# from app.core.logger import log
#
# # 最常用：带 trace_id
# log.info("创建用户成功", trace_id=request.state.trace_id)
#
# # 还可以带 user_id
# log.error("用户验证失败", trace_id=request.state.trace_id, user_id=str(user.id))
#
# # 无 trace_id 也不会报错
# log.warning("Something strange happened")