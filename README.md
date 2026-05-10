# 資料結構主題測驗網站

## 專案說明

本專案是一個使用Django框架製作的選擇題線上測驗網站，題庫內容以資料結構主題為核心。

## 功能特色

### 基本功能（必做）
- ✅ 題庫管理（可透過 Django Admin 新增／編輯題目）
- ✅ 隨機出題順序
- ✅ 作答後顯示正確答案

### 進階功能（已實現）
- ✅ 計時功能 - 測驗時顯示計時器，記錄作答時間
- ✅ 作答記錄 - 自動保存每次測驗的成績和時間
- ✅ 排行榜 - 顯示最近20次測驗成績排名
- ✅ 難易度分級 - 題目可設定簡單、中等、困難三種難度
- ✅ 錯題複習模式 - 自動記錄錯題，提供錯題列表和詳情查看
- ✅ 用戶登入/註冊系統
- ✅ 連貫題支援（保持題目順序）
- ✅ 題目圖片支援

## 專案結構

```
my final project/
├── manage.py
├── quiz_project/          # Django專案設定
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── quiz_app/              # 測驗應用程式
│   ├── models.py          # 資料模型
│   ├── views.py           # 視圖函數
│   ├── admin.py           # Admin介面
│   └── templates/quiz_app/  # HTML模板
│       ├── home.html      # 首頁
│       ├── quiz.html      # 測驗頁面
│       ├── result.html    # 結果頁面
│       ├── leaderboard.html  # 排行榜頁面
│       ├── wrong_answers.html  # 錯題列表頁面
│       └── review_wrong.html  # 錯題詳情頁面
├── import_questions.py    # 題目匯入腳本
├── 選擇題.docx           # 原始題庫
└── 說明.txt               # 專案說明
```

## 安裝與執行

### 1. 安裝依賴套件

```bash
pip install django python-docx Pillow
```

### 2. 執行資料庫遷移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 匯入題目

```bash
python import_questions.py
```

### 4. 啟動開發伺服器

```bash
python manage.py runserver
```

### 5. 建立Admin帳號

```bash
python manage.py createsuperuser
```

然後訪問 http://127.0.0.1:8000/admin/ 來管理題庫。

## 使用說明

### 開始測驗

1. 訪問 http://127.0.0.1:8000/
2. 登入或註冊帳號
3. 點擊「開始作答」進行隨機測驗
4. 回答所有題目（計時器會自動開始）
5. 提交答案查看結果

### 查看排行榜

1. 訪問 http://127.0.0.1:8000/leaderboard/
2. 查看最近20次測驗成績排名

### 錯題複習

1. 訪問 http://127.0.0.1:8000/wrong-answers/
2. 查看按測驗記錄分組的錯題
3. 點擊測驗記錄查看該次測驗的所有錯題

### 管理題庫

1. 訪問 http://127.0.0.1:8000/admin/
2. 使用Admin帳號登入
3. 在「題目」區域可以新增、編輯、刪除題目
4. 在「作答記錄」區域查看所有測驗記錄
5. 在「錯題記錄」區域查看所有錯題

## 部署到 GitHub

### 1. 創建 GitHub 倉庫

1. 登入 GitHub
2. 點擊右上角 "+" → "New repository"
3. 輸入倉庫名稱（例如：quiz-app）
4. 選擇 Public 或 Private
5. 點擊 "Create repository"

### 2. 推送到 GitHub

```bash
git remote add origin https://github.com/your-username/quiz-app.git
git branch -M main
git push -u origin main
```

### 3. 後續更新

```bash
git add .
git commit -m "更新說明"
git push
```

## 部署到雲端平台

### 選項 1: PythonAnywhere（推薦初學者）

1. 註冊 PythonAnywhere 帳號
2. 創建新的 Web 應用
3. 上傳代碼（通過 Git）
4. 配置虛擬環境
5. 安裝依賴
6. 配置 WSGI 文件
7. 設置靜態文件

### 選項 2: Render.com（免費）

1. 註冊 Render 帳號
2. 連接 GitHub 倉庫
3. 創建新的 Web Service
4. 配置構建命令和啟動命令
5. 自動部署

### 選項 3: Railway.app（免費）

1. 註冊 Railway 帳號
2. 連接 GitHub 倉庫
3. 部署 Django 應用
4. 配置環境變量

### 選項 4: Vercel（適合前端，Django 需要額外配置）

1. 註冊 Vercel 帳號
2. 連接 GitHub 倉庫
3. 配置 vercel.json
4. 部署

## 生產環境配置

### 1. 修改 settings.py

```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# 使用環境變量
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
```

### 2. 收集靜態文件

```bash
python manage.py collectstatic
```

### 3. 使用生產級數據庫

建議使用 PostgreSQL 而非 SQLite：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

## 題庫資料結構

每個題目包含以下欄位：
- `chapter`: 章節名稱
- `question_number`: 題號
- `question_text`: 題目內容
- `question_image`: 題目圖片（可選）
- `option_a`: 選項A
- `option_b`: 選項B
- `option_c`: 選項C
- `option_d`: 選項D（可選）
- `option_e`: 選項E（可選）
- `correct_answer`: 正確答案（A/B/C/D/E）
- `difficulty`: 難易度（簡單/中等/困難）
- `sequence_group`: 連貫題組別（可選）

## 目前題庫

- 第7章 樹狀結構：18題

## 技術棧

- Python 3.14
- Django 6.0.5
- SQLite
- HTML/CSS/JavaScript

## 開發者

期末專題 - 資料結構主題測驗網站