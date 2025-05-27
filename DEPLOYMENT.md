# Python教學網頁部署指南

## 🚀 Vercel部署 (推薦)

### 1. 準備工作
```bash
# 確保所有文件都已準備好
git init
git add .
git commit -m "Initial commit"
```

### 2. Vercel部署步驟

#### 方法一：使用Vercel CLI (快速)
```bash
# 安裝Vercel CLI
npm i -g vercel

# 登入Vercel
vercel login

# 部署
vercel

# 設置環境變數
vercel env add OPENAI_API_KEY
```

#### 方法二：使用GitHub + Vercel (推薦)
1. 將代碼推送到GitHub
2. 前往 [vercel.com](https://vercel.com)
3. 使用GitHub登入
4. 點擊「New Project」
5. 選擇您的repository
6. 在Environment Variables中添加：
   - `OPENAI_API_KEY`: 您的OpenAI API密鑰
7. 點擊Deploy

### 3. 配置說明
- `vercel.json`: Vercel配置文件
- `runtime.txt`: Python版本設定
- 自動檢測Flask應用

---

## 🌐 其他免費部署選項

### Railway (支持數據庫)
```bash
# 安裝Railway CLI
npm install -g @railway/cli

# 登入
railway login

# 部署
railway deploy
```

### Render
1. 前往 [render.com](https://render.com)
2. 連接GitHub
3. 選擇Web Service
4. 設置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

### Fly.io
```bash
# 安裝flyctl
# Windows: https://fly.io/docs/hands-on/install-flyctl/

# 登入
fly auth login

# 初始化
fly launch

# 部署
fly deploy
```

---

## 📊 平台比較

| 平台 | 優點 | 缺點 | PHP支持 | 數據庫 |
|------|------|------|---------|--------|
| **Vercel** | 快速、簡單、CDN | 無數據庫、運行時限制 | ✅ | ❌ |
| **Railway** | 支持數據庫、容器化 | 免費額度有限 | ✅ | ✅ PostgreSQL |
| **Render** | 全功能、支持數據庫 | 較慢的冷啟動 | ✅ | ✅ PostgreSQL |
| **Fly.io** | 全球部署、Docker | 學習曲線較陡 | ✅ | ✅ PostgreSQL |

---

## 🔄 後續PHP MySQL轉換建議

### 1. 選擇支持PHP的平台
- **Render**: 最佳選擇，支持PHP + MySQL
- **Railway**: 支持PHP + PostgreSQL/MySQL
- **Heroku**: 付費但功能完整

### 2. 數據庫選項
- **PlanetScale**: 免費MySQL (推薦)
- **Railway PostgreSQL**: 免費但有限制
- **Render PostgreSQL**: 90天免費

### 3. 轉換策略
1. 先在Vercel部署Python版本展示
2. 同時開發PHP版本
3. 使用Railway或Render部署PHP + 數據庫版本
4. 漸進式遷移

---

## 🛠️ 環境變數設置

所有平台都需要設置：
```
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here
```

---

## 📞 客戶展示URL

部署完成後，您將獲得如下格式的URL：
- Vercel: `https://your-project-name.vercel.app`
- Railway: `https://your-project-name.railway.app`
- Render: `https://your-project-name.onrender.com`

---

## 🚨 注意事項

1. **OpenAI API金鑰**: 請確保設置正確的環境變數
2. **免費額度**: 注意各平台的使用限制
3. **冷啟動**: 免費方案可能有冷啟動延遲
4. **域名**: 後續可考慮購買自定義域名 