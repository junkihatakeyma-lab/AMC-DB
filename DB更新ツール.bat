@echo off
chcp 65001 > nul
echo ------------------------------------------
echo 部品検索システム データベース更新ツール
echo ------------------------------------------
cd /d "%~dp0"
python update_all.py
pause
