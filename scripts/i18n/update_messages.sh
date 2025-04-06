#!/bin/bash

echo "🔄 更新所有已初始化语言包..."

pybabel update \
  -i messages.pot \
  -d app/i18n

echo "✅ 所有语言 .po 文件已更新"
