#!/bin/bash

echo "🔍 提取项目中的翻译文本 (_)..."

pybabel extract \
  -F babel.cfg \
  -o messages.pot \
  .

echo "✅ 已生成 messages.pot"
