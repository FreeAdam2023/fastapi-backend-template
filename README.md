app/
├── api/
│   └── v1/
│       └── endpoints/
│           ├── auth.py         ✅ 基础登录注册
│           ├── status.py       ✅ 健康检查
│           └── user.py         ✅ 用户信息获取
│       └── api.py              ✅ 汇总 router
├── core/                       ✅ 日志 / 国际化 / 配置 / 安全 / db 等
├── constants/                 ✅ token 常量
├── dependencies/              ✅ Depends 权限模块
├── schemas/                   ✅ Pydantic 模型（你还没截图，默认你有）
├── models/                    ✅ 数据库模型（你有 user、user_token）




## run server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

## init project
cd ~/Projects
./fastapi-backend-template/init_project.sh my-new-app

