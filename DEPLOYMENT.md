# 部署指南

本指南將幫助您將 Django 測驗應用部署到雲端平台。

## 部署平台選擇

### 1. PythonAnywhere（推薦初學者）

**優點：**
- 免費層可用
- 簡單易用
- 專為 Python 設計

**步驟：**

1. **註冊帳號**
   - 訪問 https://www.pythonanywhere.com/
   - 註冊免費帳號

2. **創建 Web 應用**
   - 進入 "Web" 頁面
   - 點擊 "Add a new web app"
   - 選擇 "Manual configuration"
   - 選擇 Python 版本（建議 3.10+）

3. **上傳代碼**
   - 進入 "Files" 頁面
   - 創建新目錄 `mysite`
   - 上傳所有項目文件

4. **配置虛擬環境**
   ```bash
   cd ~/mysite
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **配置 WSGI**
   - 進入 "Web" → "WSGI configuration file"
   - 替換為：
   ```python
   import os
   import sys

   path = '/home/yourusername/mysite'
   if path not in sys.path:
       sys.path.append(path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'quiz_project.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

6. **設置靜態文件**
   - 在 "Web" 頁面設置：
     - Static files: `/static/` → `/home/yourusername/mysite/staticfiles`
     - Media files: `/media/` → `/home/yourusername/mysite/media`

7. **收集靜態文件**
   ```bash
   python manage.py collectstatic
   ```

8. **設置環境變量**
   - 在 "Web" → "Environment variables" 中添加：
     - `SECRET_KEY`: 你的密鑰
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `yourusername.pythonanywhere.com`

### 2. Render.com（免費）

**優點：**
- 完全免費
- 自動部署
- 支持 GitHub 連接

**步驟：**

1. **註冊帳號**
   - 訪問 https://render.com/
   - 使用 GitHub 帳號登入

2. **連接 GitHub**
   - 進入 "Dashboard"
   - 點擊 "New +"
   - 選擇 "Web Service"

3. **配置應用**
   - 連接你的 GitHub 倉庫
   - 設置：
     - Name: `quiz-app`
     - Branch: `main`
     - Runtime: `Python 3`
     - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
     - Start Command: `gunicorn quiz_project.wsgi:application`

4. **設置環境變量**
   - 在 "Environment" 中添加：
     - `SECRET_KEY`: 你的密鑰
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `your-app.onrender.com`

5. **部署**
   - 點擊 "Create Web Service"
   - 等待部署完成

### 3. Railway.app（免費）

**優點：**
- 簡單易用
- 支持數據庫
- 免費層可用

**步驟：**

1. **註冊帳號**
   - 訪問 https://railway.app/
   - 使用 GitHub 帳號登入

2. **創建新項目**
   - 點擊 "New Project"
   - 選擇 "Deploy from GitHub repo"

3. **配置應用**
   - 選擇你的倉庫
   - Railway 會自動檢測 Django 應用

4. **設置環境變量**
   - 在 "Variables" 中添加：
     - `SECRET_KEY`: 你的密鑰
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `your-app.railway.app`

5. **部署**
   - 點擊 "Deploy"
   - 等待部署完成

### 4. Vercel（適合前端）

**優點：**
- 快速部署
- 全球 CDN
- 免費 SSL

**步驟：**

1. **註冊帳號**
   - 訪問 https://vercel.com/
   - 使用 GitHub 帳號登入

2. **創建 vercel.json**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "manage.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/static/(.*)",
         "dest": "/static/$1"
       },
       {
         "src": "/media/(.*)",
         "dest": "/media/$1"
       },
       {
         "src": "/(.*)",
         "dest": "/"
       }
     ]
   }
   ```

3. **部署**
   - 連接 GitHub 倉庫
   - Vercel 會自動部署

## 生產環境檢查清單

### 安全設置

- [ ] 設置 `DEBUG = False`
- [ ] 設置 `SECRET_KEY` 為強密碼
- [ ] 設置 `ALLOWED_HOSTS`
- [ ] 啟用 HTTPS
- [ ] 設置安全 Cookie
- [ ] 設置 CSRF 保護

### 數據庫

- [ ] 使用生產級數據庫（PostgreSQL）
- [ ] 設置數據庫連接池
- [ ] 配置數據庫備份

### 靜態文件

- [ ] 收集靜態文件
- [ ] 配置 CDN
- [ ] 設置緩存策略

### 監控

- [ ] 設置日誌記錄
- [ ] 配置錯誤追蹤
- [ ] 設置性能監控

## 常見問題

### 1. 靜態文件不顯示

確保：
- 運行了 `python manage.py collectstatic`
- 正確配置了 `STATIC_ROOT` 和 `STATIC_URL`
- Web 服務器有權訪問靜態文件目錄

### 2. 數據庫連接失敗

檢查：
- 數據庫憑證是否正確
- 數據庫是否允許遠程連接
- 防火牆設置

### 3. 502 Bad Gateway

可能原因：
- WSGI 應用未正確啟動
- 端口配置錯誤
- 應用崩潰

### 4. CSRF Token 錯誤

確保：
- `CSRF_TRUSTED_ORIGINS` 設置正確
- 使用 HTTPS
- Cookie 設置正確

## 域名設置

### 購買域名

推薦平台：
- Namecheap
- GoDaddy
- Cloudflare

### 配置 DNS

1. 在域名提供商處設置 DNS 記錄
2. 添加 A 記錄指向你的服務器 IP
3. 或添加 CNAME 記錄指向你的應用域名

### SSL 證書

大多數平台自動提供免費 SSL 證書（Let's Encrypt）。

## 備份策略

### 數據庫備份

```bash
# PostgreSQL
pg_dump dbname > backup.sql

# SQLite
cp db.sqlite3 backup.sqlite3
```

### 代碼備份

- 使用 Git 版本控制
- 定期推送到 GitHub
- 考慮使用多個遠程倉庫

## 性能優化

### 1. 數據庫優化

- 添加索引
- 使用 `select_related` 和 `prefetch_related`
- 優化查詢

### 2. 緩存

```python
# 在 settings.py 中添加
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### 3. 靜態文件 CDN

- 使用 Cloudflare
- 使用 AWS CloudFront
- 使用 Fastly

## 監控和日誌

### 日誌記錄

```python
# 在 settings.py 中添加
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

### 錯誤追蹤

推薦服務：
- Sentry
- Rollbar
- Bugsnag

## 擴展閱讀

- [Django 部署文檔](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [PythonAnywhere 教程](https://help.pythonanywhere.com/pages/Django)
- [Render Django 指南](https://render.com/docs/deploy-django)