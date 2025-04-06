#!/bin/bash

# Check if project name was passed
if [ -z "$1" ]; then
  echo "❌ Usage: ./init_project.sh <new_project_name>"
  exit 1
fi

echo "📁 Creating new FastAPI project based on boilerplate..."
cp -r ./ "$1"
cd "$1" || exit

# Cleanup old git history if exists
rm -rf .git
git init

echo "✅ Done. Project '$1' is ready."
echo "💡 Next steps:"
echo "  cd $1"
echo "  python -m venv venv && source venv/bin/activate"
echo "  pip install -r requirements.txt"
echo "  cp .env.example .env"
echo "  uvicorn main:app --reload"

