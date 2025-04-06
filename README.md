app/
├── api/
│   └── v1/
│       ├── endpoints/
│       │   ├── auth.py           # Login and authentication endpoints
│       │   ├── status.py         # Health check endpoints
│       │   └── user.py           # User-related API endpoints
│       └── api.py                # Main API router
├── core/                         # Core modules: config, logging, i18n, security, database init
├── constants/                    # Shared constants (e.g. token config)
├── dependencies/                 # Dependency injection modules (e.g. current_user, permissions)
├── schemas/                      # Pydantic schemas for request/response models
├── models/                       # Database models (e.g. User, UserToken)





## run server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug

## init project
cd ~/Projects
./fastapi-backend-template/init_project.sh my-new-app

