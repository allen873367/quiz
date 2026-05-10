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
pip install django
pip install python-docx
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
2. 選擇要測驗的章節
3. 回答所有題目（計時器會自動開始）
4. 提交答案查看結果

### 查看排行榜

1. 訪問 http://127.0.0.1:8000/leaderboard/
2. 查看最近20次測驗成績排名

### 錯題複習

1. 訪問 http://127.0.0.1:8000/wrong-answers/
2. 查看最近50道錯題
3. 點擊「查看詳情」查看完整題目和答案

### 管理題庫

1. 訪問 http://127.0.0.1:8000/admin/
2. 使用Admin帳號登入
3. 在「題目」區域可以新增、編輯、刪除題目
4. 在「作答記錄」區域查看所有測驗記錄
5. 在「錯題記錄」區域查看所有錯題

## 題庫資料結構

每個題目包含以下欄位：
- `chapter`: 章節名稱
- `question_number`: 題號
- `question_text`: 題目內容
- `option_a`: 選項A
- `option_b`: 選項B
- `option_c`: 選項C
- `option_d`: 選項D（可選）
- `option_e`: 選項E（可選）
- `correct_answer`: 正確答案（A/B/C/D/E）
- `difficulty`: 難易度（簡單/中等/困難）

## 目前題庫

- 第7章 樹狀結構：18題

## 技術棧

- Python 3.14
- Django 6.0.5
- SQLite
- HTML/CSS/JavaScript

## 開發者

期末專題 - 資料結構主題測驗網站