# Render 部署故障排除

## 查看錯誤日誌

1. 進入你的 Render Dashboard
2. 點擊你的 Web Service
3. 點擊 "Logs" 標籤
4. 查看最新的錯誤訊息

## 常見問題和解決方案

### 1. 數據庫遷移未執行

**錯誤訊息：**
```
django.db.utils.OperationalError: no such table: quiz_app_question
```

**解決方案：**

在 Render 的 Build Command 中添加遷移命令：

```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

### 2. 靜態文件問題

**錯誤訊息：**
```
Static files not found
```

**解決方案：**

確保 Build Command 包含：
```
python manage.py collectstatic --noinput
```

### 3. ALLOWED_HOSTS 問題

**錯誤訊息：**
```
Invalid HTTP_HOST header
```

**解決方案：**

在 Environment Variables 中設置：
- `ALLOWED_HOSTS`: `*` 或 `${RENDER_EXTERNAL_URL}`

### 4. 數據庫連接問題

**錯誤訊息：**
```
django.db.utils.OperationalError: could not connect to server
```

**解決方案：**

1. 創建 PostgreSQL 數據庫
2. 在 Environment Variables 中添加：
   - `DATABASE_URL`: 從數據庫頁面複製連接字符串

### 5. SECRET_KEY 問題

**錯誤訊息：**
```
django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty
```

**解決方案：**

在 Environment Variables 中設置：
- `SECRET_KEY`: 點擊 "Generate" 按鈕

## 快速修復步驟

### 步驟 1：更新 Build Command

在 Render Dashboard 中：

1. 進入你的 Web Service
2. 點擊 "Settings"
3. 找到 "Build Command"
4. 替換為：
```
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

### 步驟 2：檢查 Environment Variables

確保設置了以下環境變量：

| 變量名 | 值 |
|--------|-----|
| `SECRET_KEY` | 點擊 "Generate" |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*` |
| `DATABASE_URL` | 從 PostgreSQL 數據庫複製 |

### 步驟 3：重新部署

1. 點擊 "Manual Deploy"
2. 選擇 "Deploy latest commit"
3. 等待部署完成

### 步驟 4：查看日誌

1. 點擊 "Logs"
2. 查看是否有錯誤
3. 如果還有錯誤，複製錯誤訊息給我

## 如果問題仍然存在

請提供以下信息：

1. **錯誤日誌**：從 Render 的 Logs 頁面複製最新的錯誤訊息
2. **Build Command**：你設置的 Build Command 是什麼
3. **Start Command**：你設置的 Start Command 是什麼
4. **Environment Variables**：你設置了哪些環境變量

## 本地測試

在推送之前，先在本地測試：

```bash
# 安裝依賴
pip install -r requirements.txt

# 設置環境變量
export DEBUG=False
export SECRET_KEY="test-secret-key"
export ALLOWED_HOSTS="*"

# 運行遷移
python manage.py migrate

# 收集靜態文件
python manage.py collectstatic

# 啟動服務
python manage.py runserver
```

## 使用 SSH 進入 Render 服務器

如果需要更深入的調試：

1. 進入 Render Dashboard
2. 點擊你的 Web Service
3. 點擊 "Shell" 標籤
4. 運行以下命令：

```bash
# 查看環境變量
env | grep -E "SECRET_KEY|DEBUG|ALLOWED_HOSTS|DATABASE_URL"

# 查看數據庫遷移狀態
python manage.py showmigrations

# 手動運行遷移
python manage.py migrate

# 查看靜態文件
ls -la staticfiles/
```