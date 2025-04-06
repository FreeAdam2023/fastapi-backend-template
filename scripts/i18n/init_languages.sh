#!/bin/bash

LANGUAGES=(zh en ja ko fr de it es pt cs nl hu pl ru sv tr uk)
POT_FILE="messages.pot"
I18N_DIR="app/i18n"

echo "📦 使用模板: $POT_FILE"
echo "📁 初始化语言目录: $I18N_DIR"

for lang in "${LANGUAGES[@]}"
do
  echo "🌍 初始化语言: $lang"
  pybabel init -i "$POT_FILE" -d "$I18N_DIR" -l "$lang"
done

echo "✅ 所有语言初始化完成！"
