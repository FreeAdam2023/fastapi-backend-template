#!/bin/bash

echo "⚙️ 编译所有语言 .mo 文件..."

pybabel compile \
  -d app/i18n

echo "✅ 编译完成，语言包可用！"
