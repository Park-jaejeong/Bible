@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo ====================================================
echo  개역개정 성경 웹 뷰어를 웹 브라우저에서 실행합니다.
echo  주소: http://localhost:8080
echo ====================================================
start "" "http://localhost:8080"
python -m http.server 8080
pause
