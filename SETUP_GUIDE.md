# 快速設置指南 🚀

## 第一次使用？跟著這些步驟走！

### 1️⃣ 安裝依賴套件
```bash
pip install -r requirements.txt
```

### 2️⃣ 設定環境變數
```bash
# 複製環境變數範例文件
copy env.example .env

# 編輯 .env 文件，填入您的OpenAI API金鑰
# OPENAI_API_KEY=your-api-key-here
```

### 3️⃣ 獲取OpenAI API金鑰
1. 前往 [OpenAI官網](https://platform.openai.com/api-keys)
2. 登入或註冊帳戶
3. 點擊 "Create new secret key"
4. 複製API金鑰到 `.env` 文件

### 4️⃣ 啟動網站
選擇其中一種方式：

**方式一：直接執行**
```bash
python app.py
```

**方式二：使用批次檔（Windows）**
```bash
start.bat
```

**方式三：使用PowerShell腳本**
```bash
.\start.ps1
```

### 5️⃣ 打開瀏覽器
訪問：`http://localhost:5000`

## 🎯 主要功能

- **首頁** - 平台介紹和功能概覽
- **課程** - 7個系統化Python教學章節
- **AI助教** - 24/7在線AI助教服務
- **程式練習** - 10個練習題目和在線編輯器

## 🔧 常見問題

**Q: 啟動時出現模組未找到錯誤？**
A: 執行 `pip install -r requirements.txt` 安裝依賴

**Q: AI助教無法回應？**
A: 檢查 `.env` 文件中的 `OPENAI_API_KEY` 是否正確設定

**Q: 網站無法訪問？**
A: 確認控制台有顯示 "Running on http://127.0.0.1:5000"

**Q: 想要修改端口？**
A: 在 `.env` 文件中設定 `PORT=您想要的端口號`

## 📞 需要幫助？

- 查看 `README.md` 獲取詳細文檔
- 檢查控制台錯誤訊息
- 確認所有依賴都已正確安裝

## 🎉 開始學習Python吧！

設置完成後，您就可以開始使用這個現代化的Python學習平台了！ 