# 資料結構主題測驗網站

## 專案說明

本專案是一個使用 Django 6.0.5 框架製作的選擇題線上測驗網站，題庫內容以資料結構「樹狀結構」為核心（第7章，共23題，含教師題目與自編題目）。採用「Aurora Glass」極光玻璃主題設計。

## 功能特色

### 測驗系統
- **主題測驗** — 針對第7章樹狀結構進行測驗
- **隨機挑戰** — 跨章節混合出題
- **自訂題數** — 可選擇 5 / 10 / 15 / 20 / 全部 題數
- **間隔學習 (Spaced Repetition)** — 答錯的題目自動記錄，最多三輪強化，幫助真正搞懂
- **計時功能** — 測驗時顯示計時器，記錄作答時間
- **即時回饋** — 每題作答後立即顯示正確／錯誤與詳細解析
- **交卷機制** — 全部答完自動提交；可提前交卷，未完成時會提示

### 排行榜系統
- **一般排行** — 分數排名（前20名）
- **間隔學習排行** — 按完成速度排名

### 學習記錄
- **作答記錄** — 自動保存每次測驗的成績、時間、章節
- **錯題複習** — 自動記錄錯題，提供按測驗記錄分組的錯題列表
- **錯題詳情** — 查看每道錯題的題目、正確答案與詳細解析

### 管理後台（自訂管理面板）
- **題目管理** — 新增、編輯、刪除題目（含圖片上傳）
- **批次操作** — 支援全選批次刪除題目、用戶、記錄
- **用戶管理** — 編輯用戶暱稱、Email、密碼、管理員權限，新增／刪除用戶
- **測驗記錄管理** — 檢視與刪除測驗記錄
- **系統資訊** — 題庫總數、自編題數、用戶數、測驗次數、章節數

### 用戶系統
- **註冊／登入／登出**
- **個人資料管理** — 點擊右上角暱稱標籤即可修改暱稱、Email、密碼
- **帳號刪除** — 使用者可自行刪除自己的帳號

### 使用者體驗
- **Aurora Glass 主題** — 深紫藍漸層背景、玻璃擬態卡片、圓角按鈕
- **響應式設計** — 支援桌面與行動裝置
- **繁體中文介面**

## 專案結構

```
my final project/
├── manage.py
├── quiz_project/                  # Django 專案設定
│   ├── settings.py                # 設定檔
│   └── urls.py                    # URL 路由
├── quiz_app/                      # 測驗應用程式
│   ├── models.py                  # 資料模型 (User, Question, QuizRecord, WrongAnswer)
│   ├── views.py                   # 視圖函數與 API 端點
│   ├── admin.py                   # Django Admin 設定
│   ├── static/quiz_app/
│   │   ├── css/style.css          # Aurora Glass 主題樣式
│   │   └── images/                # 題目圖片
│   └── templates/quiz_app/
│       ├── home.html              # 首頁
│       ├── quiz.html              # 測驗設定頁面
│       ├── take_quiz.html         # 作答頁面
│       ├── result.html            # 答題結果頁面
│       ├── leaderboard.html       # 排行榜（一般＋間隔學習）
│       ├── quiz_records.html      # 個人測驗記錄
│       ├── wrong_answers.html     # 錯題列表
│       ├── wrong_answers_detail.html # 錯題詳情
│       ├── review_wrong.html      # 錯題複習
│       ├── login.html             # 登入頁面
│       ├── register.html          # 註冊頁面
│       └── admin_panel.html       # 自訂管理後台
└── import_questions.py            # 題目匯入腳本
```

## API 端點

### 個人資料
| 方法 | 路徑 | 說明 |
|------|------|------|
| POST | `/api/profile/update/` | 更新暱稱、Email |
| POST | `/api/profile/change-password/` | 更改密碼（需舊密碼） |
| POST | `/api/profile/delete/` | 刪除自己的帳號 |

### 管理後台 API
| 方法 | 路徑 | 說明 |
|------|------|------|
| GET | `/admin-panel/api/question/{id}/` | 取得單題資料 |
| POST | `/admin-panel/api/question/{id}/update/` | 更新題目 |
| POST | `/admin-panel/api/question/{id}/delete/` | 刪除題目 |
| POST | `/admin-panel/api/question/create/` | 新增題目 |
| POST | `/admin-panel/api/user/{id}/update/` | 更新用戶 |
| POST | `/admin-panel/api/user/{id}/delete/` | 刪除用戶 |
| POST | `/admin-panel/api/user/create/` | 新增用戶 |
| POST | `/admin-panel/api/record/{id}/delete/` | 刪除記錄 |
| POST | `/admin-panel/api/batch-delete/` | 批次刪除 |

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

### 3. 匯入題目（可選，已有範例資料）

```bash
python import_questions.py
```

### 4. 啟動開發伺服器

```bash
python manage.py runserver
```

### 5. 建立管理員帳號

```bash
python manage.py createsuperuser
```

## 使用說明

### 開始測驗
1. 訪問 http://127.0.0.1:8000/
2. 登入或註冊帳號
3. 選擇「第7章 樹狀結構」或「隨機挑戰」
4. 設定題數（5/10/15/20/全部）、間隔學習開關
5. 點擊「開始作答」
6. 每題作答後立即顯示正確／錯誤與解析
7. 全部答完後點擊「提交答案」或右上角「交卷」

### 查看排行榜
1. 一般排行：http://127.0.0.1:8000/leaderboard/
2. 間隔學習排行：http://127.0.0.1:8000/leaderboard/sr/

### 錯題複習
1. 訪問 http://127.0.0.1:8000/wrong-answers/
2. 查看按測驗記錄分組的錯題
3. 點擊測驗記錄查看該次測驗的所有錯題與解析

### 個人資料管理
1. 點擊右上角的暱稱標籤（淡紫色圓角）
2. 在彈窗中修改暱稱、Email
3. 輸入舊密碼與新密碼可更改密碼
4. 輸入 `DELETE` 可永久刪除帳號

### 管理後台（需管理員權限）
1. 訪問 http://127.0.0.1:8000/admin-panel/
2. 使用管理員帳號登入
3. **題目管理**：搜尋、篩選、新增、編輯（含圖片）、批次刪除
4. **用戶管理**：編輯（暱稱/Email/管理員權限）、新增、批次刪除
5. **測驗記錄**：檢視、單筆刪除、批次刪除
6. 也可使用 Django 原生後台：http://127.0.0.1:8000/admin/

## 題庫資料結構

每個題目包含以下欄位：

| 欄位 | 說明 |
|------|------|
| `chapter` | 章節名稱（第7章 樹狀結構） |
| `question_number` | 題號 |
| `question_text` | 題目內容 |
| `question_image` | 題目圖片（可選） |
| `option_a` ~ `option_e` | 選項 A~E |
| `correct_answer` | 正確答案（A/B/C/D/E） |
| `difficulty` | 難易度（簡單/中等/困難） |
| `explanation` | 題目詳解 |
| `is_new` | 是否為自編題目 |
| `sequence_group` | 連貫題組別（可選） |

## 目前題庫

- 第7章 樹狀結構：**23 題**（含教師題目 + 自編題目）
- 全部題目皆有完整詳解

## 技術棧

- Python 3.14
- Django 6.0.5
- SQLite
- HTML / CSS / JavaScript
- Aurora Glass（極光玻璃）主題

## 開發者

CBF113007鄭書懷
CBF113018郭漢廷