# Python教學網站啟動腳本
Write-Host "=== Python程式設計教學網站 ===" -ForegroundColor Green
Write-Host ""

# 檢查Python是否安裝
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到Python，請先安裝Python 3.8或更新版本" -ForegroundColor Red
    exit 1
}

# 檢查依賴是否安裝
Write-Host "📦 檢查依賴套件..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "✅ requirements.txt 存在" -ForegroundColor Green
} else {
    Write-Host "❌ 未找到 requirements.txt" -ForegroundColor Red
    exit 1
}

# 檢查環境變數文件
Write-Host "🔧 檢查環境配置..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env 文件存在" -ForegroundColor Green
} else {
    Write-Host "⚠️  未找到 .env 文件" -ForegroundColor Yellow
    Write-Host "   請複製 env.example 為 .env 並填入正確的配置" -ForegroundColor Yellow
    Write-Host "   特別是 OPENAI_API_KEY 需要設定您的OpenAI API金鑰" -ForegroundColor Yellow
}

# 檢查虛擬環境
if (Test-Path ".venv") {
    Write-Host "🐍 檢測到虛擬環境，正在啟動..." -ForegroundColor Cyan
    & ".venv/Scripts/Activate.ps1"
}

Write-Host ""
Write-Host "🚀 正在啟動應用程式..." -ForegroundColor Green
Write-Host "📍 網站地址: http://localhost:5000" -ForegroundColor Cyan
Write-Host "⚠️  請在瀏覽器中打開上述地址訪問網站" -ForegroundColor Yellow
Write-Host "🛑 按 Ctrl+C 停止服務" -ForegroundColor Red
Write-Host ""

# 啟動Flask應用
try {
    python app.py
} catch {
    Write-Host "❌ 啟動失敗，請檢查錯誤訊息" -ForegroundColor Red
    Write-Host "💡 常見解決方法:" -ForegroundColor Yellow
    Write-Host "   1. 執行: pip install -r requirements.txt" -ForegroundColor Yellow
    Write-Host "   2. 檢查 .env 文件是否正確配置" -ForegroundColor Yellow
    Write-Host "   3. 確認 OPENAI_API_KEY 已設定" -ForegroundColor Yellow
}

Write-Host "按任意鍵退出..." -ForegroundColor Gray
Read-Host 