<<<<<<< HEAD
# 🌳 資料結構主題測驗網站

> **Aurora Glass** 極光玻璃主題 × Django 6.0.5 線上測驗平台

本專案是一個以資料結構「樹狀結構」為核心的選擇題線上測驗網站，採用現代玻璃擬態（Glassmorphism）搭配深紫藍漸層背景，提供完整的測驗、排行、錯題複習與管理功能。

---

## ✨ 功能特色

### 📝 測驗系統
| 功能 | 說明 |
|------|------|
| **主題測驗** | 針對第7章樹狀結構 23 題進行測驗 |
| **隨機挑戰** | 跨章節混合出題，自由選擇範圍 |
| **自訂題數** | 5 / 10 / 15 / 20 / 全部，彈性選擇 |
| **連貫題保護** | 連貫題組（如 11→12→13）整組出現，不被拆散 |
| **間隔學習（SR）** | 答錯的題目自動進入下一輪，直到全部答對為止，無上限次數 |
| **SR 評分** | 以第一輪答對數作為最終評分，後面輪次只為鞏固學習 |
| **即時回饋** | 每題作答後立即顯示正確／錯誤與詳細解析 |
| **計時功能** | 測驗過程顯示即時計時器 |

### 🏆 排行榜
- **一般排行** — 依分數排名（前 20 名）
- **間隔學習排行** — 依完成速度排名（前 20 名）
- **篩選功能** — 支援章節與題數篩選

### 📊 學習記錄
- **作答記錄** — 每次測驗的成績、時間、章節自動保存
- **錯題複習** — 按測驗記錄分組的錯題列表
- **錯題詳情** — 查看每道錯題的題目、正確答案與完整解析

### 🔧 管理後台
- **題目管理** — 新增、編輯、刪除題目（支援圖片上傳）
- **批次操作** — 全選批次刪除題目、用戶、記錄
- **用戶管理** — 編輯暱稱／Email／管理員權限，新增與刪除用戶
- **測驗記錄管理** — 檢視與刪除測驗記錄
- **系統資訊** — 題庫總數、自編題數、用戶數、測驗次數總覽

### 👤 用戶系統
- 註冊／登入／登出
- **個人資料管理** — 點擊右上角暱稱即可修改暱稱、Email、密碼
- **帳號刪除** — 使用者可自行永久刪除帳號

### 🎨 視覺體驗
- **Aurora Glass 主題** — 深紫藍漸層背景、玻璃擬態卡片、圓角按鈕
- **動態流星雨** — 首頁背景流星滑落效果
- **游標光暈** — 滑鼠移動時跟隨的極光光暈
- **繁體中文** — 全站繁體中文介面

---

## 📁 專案結構

```
my final project/
├── manage.py
├── import_questions.py              # 題目匯入腳本
├── quiz_project/                    # Django 專案設定
│   ├── settings.py
│   └── urls.py
└── quiz_app/                        # 測驗應用程式
    ├── models.py                    # User / Question / QuizRecord / WrongAnswer
    ├── views.py                     # 視圖函數 + RESTful API 端點
    ├── admin.py                     # Django 原生 Admin 設定
    ├── management/commands/
    │   └── import_questions.py      # Django 指令式匯入
    ├── static/quiz_app/
    │   ├── css/style.css            # Aurora Glass 完整主題樣式
    │   └── images/                  # 題目圖片存放
    └── templates/
        ├── admin/
        │   └── base_site.html       # Django 原生 Admin 美化
        └── quiz_app/
            ├── home.html            # 首頁（流星雨 + 游標光暈）
            ├── quiz.html            # 測驗設定頁
            ├── take_quiz.html       # 作答頁
            ├── result.html          # 結果頁
            ├── leaderboard.html     # 排行榜（一般 + SR）
            ├── quiz_records.html    # 測驗記錄
            ├── wrong_answers.html   # 錯題列表
            ├── wrong_answers_detail.html  # 錯題詳情
            ├── review_wrong.html    # 單題錯題複習
            ├── random_quiz_setup.html     # 隨機挑戰設定
            ├── login.html           # 登入
            ├── register.html        # 註冊
            └── admin_panel.html     # 自訂管理後台
```

---

## 🔌 API 端點

### 個人資料

| 方法 | 路徑 | 說明 |
|------|------|------|
| `POST` | `/api/profile/update/` | 更新暱稱、Email |
| `POST` | `/api/profile/change-password/` | 更改密碼（需提供舊密碼） |
| `POST` | `/api/profile/delete/` | 永久刪除自己的帳號 |

### 管理後台 API

| 方法 | 路徑 | 說明 |
|------|------|------|
| `GET` | `/admin-panel/api/question/{id}/` | 取得單題資料（JSON） |
| `POST` | `/admin-panel/api/question/{id}/update/` | 更新題目 |
| `POST` | `/admin-panel/api/question/{id}/delete/` | 刪除題目 |
| `POST` | `/admin-panel/api/question/create/` | 新增題目 |
| `POST` | `/admin-panel/api/user/{id}/update/` | 更新用戶資料 |
| `POST` | `/admin-panel/api/user/{id}/delete/` | 刪除用戶 |
| `POST` | `/admin-panel/api/user/create/` | 新增用戶 |
| `POST` | `/admin-panel/api/record/{id}/delete/` | 刪除測驗記錄 |
| `POST` | `/admin-panel/api/batch-delete/` | 批次刪除（題目／用戶／記錄） |

---

## 🚀 安裝與執行

### 前置需求
- Python 3.14+
- pip

### 1. 安裝依賴套件

```bash
pip install django python-docx Pillow
```

### 2. 資料庫遷移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 匯入題庫（已有範例資料則可跳過）

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

### 6. 開啟瀏覽器

訪問 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📖 使用指南

### 開始測驗
1. 訪問首頁 → 註冊／登入
2. 選擇「第7章 樹狀結構」或「隨機挑戰」
3. 設定題數（5/10/15/20/全部）與間隔學習模式
4. 開始作答，每題送出後立即顯示對錯與解析
5. 全部完成後自動提交結算

### 間隔學習模式
- **第一輪**：正常作答，記錄答對數作為評分依據
- **後續輪次**：只出現答錯的題目，答對的題目不再出現
- **無上限次數**：持續到所有題目答對為止
- **排行榜**：依總完成時間排名

### 管理後台
1. 訪問 `/admin-panel/` 並以管理員帳號登入
2. 題目管理：搜尋、篩選、編輯、新增、批次刪除
3. 用戶管理：編輯權限、新增、刪除
4. 也可使用 Django 原生後台 `/admin/`

---

## 🗃️ 題庫資料結構

| 欄位 | 型態 | 說明 |
|------|------|------|
| `chapter` | `CharField` | 章節名稱 |
| `question_number` | `IntegerField` | 題號 |
| `question_text` | `TextField` | 題目內容 |
| `question_image` | `ImageField` | 題目圖片（可選） |
| `option_a` ~ `option_e` | `CharField` | 選項 A~E（D、E 可選） |
| `correct_answer` | `CharField` | 正確答案（A/B/C/D/E） |
| `difficulty` | `CharField` | 難易度：簡單 / 中等 / 困難 |
| `explanation` | `TextField` | 題目詳解 |
| `is_new` | `BooleanField` | 是否為自編題目 |
| `source_note` | `CharField` | 題目來源說明 |
| `sequence_group` | `CharField` | 連貫題組別（同組整題出現） |

### 目前題庫
- **第7章 樹狀結構**：23 題（含教師題目 + 自編題目）
- **連貫題組**：題號 11→12→13 為一組，系統自動整組保留
- 全部題目皆有完整詳解

---

## 🛠️ 技術棧

| 技術 | 版本 |
|------|------|
| Python | 3.14 |
| Django | 6.0.5 |
| 資料庫 | SQLite |
| 前端 | HTML / CSS / JavaScript |
| 主題 | Aurora Glass（極光玻璃） |
| 圖片處理 | Pillow |

---

## 👨‍💻 開發者

- **CBF113007** 鄭書懷
- **CBF113018** 郭漢廷

*資料結構期末專題 — 樹狀結構主題測驗網站*
=======
# hanting-team-
期末專題
>>>>>>> 421d36d5e111f2fd8458385b15a70fc2f4c9f5f1
