# 資料結構主題測驗網站

> **Cosmic Ocean** 宇宙深空主題 × Django 6.0 線上測驗平台

本專案是一個完整的資料結構選擇題線上測驗平台，採用深空宇宙視覺主題，支援完整的測驗、排行、錯題複習、學習分析、班級管理與管理後台功能。

---

## 功能特色

### 測驗系統
| 功能 | 說明 |
|------|------|
| **主題測驗** | 針對各章節進行測驗（樹狀結構、圖形、排序等） |
| **隨機挑戰** | 跨章節混合出題，自由選擇章節範圍與題數 |
| **自訂題數** | 5 / 10 / 15 / 20 / 全部，彈性選擇 |
| **連貫題保護** | 連貫題組保持順序，整組出現不被拆散 |
| **間隔學習（SR）** | 答錯的題目自動進入下一輪，直到全部答對，無上限次數 |
| **SR 評分** | 以第一輪答對數作為最終評分，後續輪次只為鞏固學習 |
| **即時回饋** | 每題作答後立即顯示正確／錯誤與詳細解析 |
| **計時功能** | 測驗過程顯示即時計時器 |

### 學習數據與圖表分析
- **個人雷達圖** — 在記錄頁面以 Chart.js 雷達圖顯示各章節正確率，一眼看出弱點
- **分數趨勢圖** — 折線圖呈現學習進步趨勢
- **魔王題標記** — 系統自動計算每題錯誤率，錯誤率 ≥ 70% 且答題 ≥ 5 次的題目標示為魔王題

### 排行榜
- **一般排行** — 依分數排名（前 20 名）
- **間隔學習排行** — 依完成速度排名（前 20 名）
- **篩選功能** — 支援章節與題數篩選

### 學習記錄
- **作答記錄** — 每次測驗的成績、時間、章節自動保存
- **錯題複習** — 按測驗記錄分組的錯題列表
- **錯題詳情** — 查看每道錯題的題目、正確答案與完整解析
- **PDF 報表匯出** — 將學習歷程匯出為精美 HTML 報告，可用瀏覽器「列印 → 另存 PDF」下載（含各章節表現統計）

### 班級與群組功能
- **教師角色** — 管理員可設定為教師身分，建立班級房間
- **邀請碼系統** — 每個班級產生唯一 6 位邀請碼
- **班級儀表板** — 教師可檢視全班學生測驗次數、平均分數、正確率
- **常見錯題 TOP 10** — 系統自動統計全班錯誤最多的題目，方便課堂針對性講解
- **學生加入** — 學生可透過邀請碼加入班級

### 管理後台
- **題目管理** — 新增、編輯、刪除題目（支援圖片上傳）
- **CSV 批次匯入** — 上傳 CSV 檔案一次匯入多題，支援覆寫模式
- **CSV 批次匯出** — 將題庫匯出為 CSV 檔
- **批次操作** — 全選批次刪除題目、用戶、記錄
- **用戶管理** — 編輯暱稱／Email／管理員權限，新增與刪除用戶
- **班級帳號** — 批次建立班級學生帳號（如 `資工二甲01` ~ `資工二甲40`）
- **系統資訊面板** — 使用人數、上線人數、答題次數統計、各章節答題分布

### 用戶系統
- 註冊／登入／登出
- **個人資料管理** — 點擊右上角暱稱即可修改暱稱、Email、密碼
- **班級設定** — 管理員可為用戶設定班級
- **帳號刪除** — 使用者可自行永久刪除帳號

### 視覺體驗 —「Cosmic Ocean」主題
- **深空宇宙配色** — 深藍色基底搭配電光青（Cyan）與紫羅蘭（Violet）輔色
- **CSS 動態星空** — 24 顆閃爍星點粒子背景
- **浮動光暈** — 3 個彩色漸層光暈在背景緩慢漂浮
- **玻璃擬態卡片** — 毛玻璃效果搭配旋轉漸變邊框動畫
- **高階按鈕系統** — 鏡面掃光效果、霓虹發光陰影、按壓縮放回饋
- **滾動揭示動畫** — 區塊進入視口時優雅淡入
- **完全繁體中文** — 全站繁體中文介面

---

## 系統需求

- **Python 3.10+**（建議 3.12 以上）
- **pip**（Python 套件管理器）
- **Git**（選用，用於版本控制）

---

## 快速安裝（5 分鐘）

### 1. 取得專案

```bash
# 下載專案 ZIP 或使用 Git Clone
git clone https://github.com/allen873367/quiz.git
cd quiz
```

### 2. 建立虛擬環境（強烈建議）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 4. 資料庫遷移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 匯入題庫

```bash
python import_questions.py
```

匯入腳本會自動建立各章節的題目資料（第 1~13 章），包含自編題目與連貫題組標記。

### 6. 建立管理員帳號

```bash
python manage.py createsuperuser
```

依序輸入帳號、Email（可略過）、密碼。

### 7. 設定教師身分

以管理員身分登入 Django 後台 `/admin/`，找到你的用戶帳號，勾選 **`is_teacher`** 欄位並儲存，即可使用班級管理功能。

### 8. 啟動開發伺服器

```bash
python manage.py runserver
```

### 9. 開啟瀏覽器

訪問 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** 即可開始使用。

---

## 進階設定

### 環境變數（選用）

在專案根目錄建立 `.env` 檔案，可覆寫以下設定：

```env
# 安全金鑰（生產環境務必自訂）
SECRET_KEY=your-secret-key-here

# 除錯模式（生產環境設為 False）
DEBUG=False

# 允許的主機（多個用逗號分隔）
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# PostgreSQL 連線字串（預設使用 SQLite）
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### 生產環境部署

```bash
# 收集靜態檔案
python manage.py collectstatic --noinput

# 使用 Gunicorn 啟動（Linux）
gunicorn quiz_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

> 若使用 **ngrok** 對外公開測試，請在 `settings.py` 的 `CSRF_TRUSTED_ORIGINS` 中加入你的 ngrok 網址。

---

## 專案結構

```
quiz/
├── manage.py                     # Django 管理指令入口
├── requirements.txt              # Python 依賴套件
├── import_questions.py           # 題目匯入腳本（第7章）
├── db.sqlite3                    # SQLite 資料庫（執行 migrate 後產生）
├── .env                          # 環境變數設定（選用）
├── README.md                     # 本檔案
│
├── 資料結構題目/                  # CSV 題庫檔（匯入用）
│   ├── ch01_xxx.csv
│   ├── ch02_xxx.csv
│   └── ...
│
├── quiz_project/                 # Django 專案設定
│   ├── settings.py               # 設定檔（資料庫、套件、靜態檔案）
│   └── urls.py                   # URL 路由
│
├── quiz_app/                     # 測驗應用程式
│   ├── models.py                 # 資料模型（User / Question / QuizRecord ...）
│   ├── views.py                  # 主要視圖函數 + API 端點
│   ├── admin.py                  # Django 原生 Admin 設定
│   ├── templatetags/             # 自訂模板標籤
│   │   ├── __init__.py
│   │   └── chapter_extras.py     # 章節名稱處理濾器
│   ├── management/commands/
│   │   └── import_questions.py   # Django 指令式匯入
│   ├── static/quiz_app/
│   │   ├── css/style.css         # Cosmic Ocean 完整主題樣式
│   │   └── images/               # 題目圖片存放
│   └── templates/
│       ├── admin/
│       │   └── base_site.html    # Django 原生 Admin 美化
│       └── quiz_app/
│           ├── home.html         # 首頁
│           ├── quiz.html         # 測驗設定頁
│           ├── take_quiz.html    # 作答頁
│           ├── result.html       # 結果頁
│           ├── leaderboard.html  # 排行榜
│           ├── quiz_records.html # 測驗記錄 + Chart.js 圖表
│           ├── wrong_answers.html
│           ├── wrong_answers_detail.html
│           ├── review_wrong.html
│           ├── random_quiz_setup.html
│           ├── login.html
│           ├── register.html
│           ├── admin_panel.html  # 自訂管理後台
│           ├── classroom_list.html
│           ├── classroom_detail.html
│           ├── classroom_my.html
│           └── pdf_report.html   # 學習歷程報表
│
├── media/                        # 使用者上傳檔案（自動產生）
└── staticfiles/                  # 收集的靜態檔案（collectstatic）
```

---

## 使用指南

### 開始測驗
1. 訪問首頁 → 註冊／登入
2. 選擇章節（如「第7章 樹狀結構」）或「隨機挑戰」
3. 設定題數與間隔學習模式
4. 開始作答，每題送出後立即顯示對錯與解析
5. 全部完成後自動提交結算

### 觀看學習分析
1. 登入後點擊導航列「紀錄」
2. 點擊「學習分析」面板展開
3. 查看雷達圖（各章節正確率）與分數趨勢圖

### 間隔學習模式
- **第一輪**：正常作答，記錄答對數作為評分依據
- **後續輪次**：只出現答錯的題目，答對的題目不再出現
- **無上限次數**：持續到所有題目答對為止
- **排行榜**：依總完成時間排名

### 教師使用班級功能
1. 登入後點擊導航列「課程」
2. 點擊「＋ 建立班級」，系統自動產生邀請碼
3. 分享邀請碼給學生
4. 學生點擊「加入班級」輸入邀請碼即可
5. 點擊班級卡片進入儀表板，查看學生表現與常見錯題

### 匯出學習歷程 PDF
1. 登入後點擊導航列「紀錄」
2. 點擊「學習分析」展開面板
3. 點擊「學習歷程報表」開啟報表頁
4. 點擊「列印／另存 PDF」按鈕，選擇「另存 PDF」即可下載

### 管理後台
1. 訪問 `/admin-panel/` 並以管理員帳號登入
2. **題目管理**：搜尋、篩選、編輯、新增、批次刪除題目
3. **CSV 匯入**：點擊「匯入 CSV」上傳檔案批次新增題目
4. **CSV 匯出**：點擊「匯出 CSV」下載題庫
5. **魔王題面板**：點擊側邊欄「魔王題」查看高錯誤率題目
6. **用戶管理**：編輯權限、新增、刪除用戶
7. **資訊面板**：系統統計資料總覽
8. 也可使用 Django 原生後台 `/admin/`

---

## API 端點

### 個人資料
| 方法 | 路徑 | 說明 |
|------|------|------|
| `POST` | `/api/profile/update/` | 更新暱稱、Email |
| `POST` | `/api/profile/change-password/` | 更改密碼（需提供舊密碼） |
| `POST` | `/api/profile/delete/` | 永久刪除自己的帳號 |

### 學習圖表分析
| 方法 | 路徑 | 說明 |
|------|------|------|
| `GET` | `/api/my-chapter-stats/` | 各章節正確率（Chart.js 雷達圖用） |
| `GET` | `/api/quiz-timeline/` | 歷次測驗分數趨勢（折線圖用） |
| `GET` | `/admin-panel/api/stats/boss-questions/` | 魔王題列表（錯誤率 ≥ 70%） |

### 班級管理
| 方法 | 路徑 | 說明 |
|------|------|------|
| `POST` | `/api/classroom/create/` | 教師建立班級（含邀請碼） |
| `POST` | `/api/classroom/join/` | 學生透過邀請碼加入班級 |
| `GET` | `/classroom/` | 教師班級列表 |
| `GET` | `/classroom/{id}/` | 班級儀表板（學生表現 + 常見錯題） |
| `GET` | `/classroom/my/` | 學生的已加入班級列表 |

### CSV 匯入/匯出
| 方法 | 路徑 | 說明 |
|------|------|------|
| `GET` | `/admin-panel/export/csv/` | 匯出題庫 CSV |
| `POST` | `/admin-panel/import/csv/` | 批次匯入題庫 CSV |

### PDF 報表
| 方法 | 路徑 | 說明 |
|------|------|------|
| `GET` | `/export/pdf/` | 下載個人學習歷程 PDF 報表 |

### 管理後台 API
| 方法 | 路徑 | 說明 |
|------|------|------|
| `GET` | `/admin-panel/api/stats/overview/` | 系統資訊總覽 |
| `GET` | `/admin-panel/api/stats/user-errors/` | 使用者錯誤率統計 |
| `GET` | `/admin-panel/api/stats/question-errors/` | 題目錯誤率與選項分布 |
| `GET` | `/admin-panel/api/question/{id}/` | 取得單題資料 |
| `POST` | `/admin-panel/api/question/{id}/update/` | 更新題目 |
| `POST` | `/admin-panel/api/question/{id}/delete/` | 刪除題目 |
| `POST` | `/admin-panel/api/question/create/` | 新增題目 |
| `POST` | `/admin-panel/api/user/{id}/update/` | 更新用戶 |
| `POST` | `/admin-panel/api/user/{id}/delete/` | 刪除用戶 |
| `POST` | `/admin-panel/api/user/create/` | 新增用戶 |
| `POST` | `/admin-panel/api/record/{id}/delete/` | 刪除測驗記錄 |
| `POST` | `/admin-panel/api/batch-delete/` | 批次刪除 |
| `POST` | `/admin-panel/api/class/create/` | 批次建立班級帳號 |
| `POST` | `/admin-panel/api/class/delete/` | 刪除整班帳號 |

---

## 資料庫模型

### User（使用者）
| 欄位 | 型態 | 說明 |
|------|------|------|
| `username` | `CharField` | 帳號 |
| `nickname` | `CharField` | 暱稱 |
| `email` | `EmailField` | 電子郵件 |
| `student_class` | `CharField` | 班級（如 資工二甲） |
| `is_teacher` | `BooleanField` | 教師身分 |
| `is_staff` | `BooleanField` | 管理員權限 |

### Question（題目）
| 欄位 | 型態 | 說明 |
|------|------|------|
| `chapter` | `CharField` | 章節名稱（如「第7章 樹狀結構」） |
| `question_number` | `IntegerField` | 題號 |
| `question_text` | `TextField` | 題目內容 |
| `question_image` | `ImageField` | 題目圖片（可選） |
| `option_a` ~ `option_e` | `CharField` | 選項 A~E（D、E 可選） |
| `correct_answer` | `CharField` | 正確答案（A/B/C/D/E） |
| `difficulty` | `CharField` | 難易度（easy / medium / hard） |
| `explanation` | `TextField` | 題目詳解 |
| `is_new` | `BooleanField` | 是否為自編題目 |
| `source_note` | `CharField` | 題目來源說明 |
| `sequence_group` | `CharField` | 連貫題組別 |
| `error_count` | `IntegerField` | 累計錯誤次數 |
| `total_attempt_count` | `IntegerField` | 累計答題次數 |

### QuizRecord（測驗記錄）
| 欄位 | 型態 | 說明 |
|------|------|------|
| `user` | `ForeignKey(User)` | 作答者 |
| `chapter` | `CharField` | 章節名稱 |
| `score` | `IntegerField` | 分數（答對題數） |
| `total_questions` | `IntegerField` | 總題數 |
| `time_taken` | `IntegerField` | 作答時間（秒） |
| `is_sr` | `BooleanField` | 是否為間隔學習模式 |
| `created_at` | `DateTimeField` | 測驗時間 |

### WrongAnswer（錯題記錄）
| 欄位 | 型態 | 說明 |
|------|------|------|
| `quiz_record` | `ForeignKey(QuizRecord)` | 所屬測驗記錄 |
| `question` | `ForeignKey(Question)` | 錯誤的題目 |
| `selected_answer` | `CharField` | 使用者選擇的答案 |
| `correct_answer` | `CharField` | 正確答案 |
| `created_at` | `DateTimeField` | 記錄時間 |

### Classroom（班級）
| 欄位 | 型態 | 說明 |
|------|------|------|
| `name` | `CharField` | 班級名稱 |
| `teacher` | `ForeignKey(User)` | 教師 |
| `invite_code` | `CharField` | 6 位邀請碼 |
| `is_active` | `BooleanField` | 啟用狀態 |

### ClassroomEnrollment（班級成員）
| 欄位 | 型態 | 說明 |
|------|------|------|
| `classroom` | `ForeignKey(Classroom)` | 班級 |
| `student` | `ForeignKey(User)` | 學生 |
| `joined_at` | `DateTimeField` | 加入時間 |

---

## 技術棧

| 技術 | 用途 |
|------|------|
| **Python 3.14** | 程式語言 |
| **Django 6.0** | Web 框架 |
| **SQLite / PostgreSQL** | 資料庫（開發用 SQLite，生產可換 PostgreSQL） |
| **Chart.js 4.4** | 前端圖表分析（雷達圖 + 折線圖） |
| **HTML Print (CSS @page)** | PDF 報表生成 |
| **CSS3 (Custom Properties)** | Cosmic Ocean 深空主題 |
| **Pillow** | 圖片處理 |
| **WhiteNoise** | 靜態檔案服務（生產環境） |
| **Gunicorn** | WSGI 伺服器（Linux 生產環境） |
| **dj-database-url** | 資料庫連線字串解析 |
| **python-dotenv** | 環境變數管理 |

---

## 疑難排解

### 1. 管理後台顯示 500 錯誤（`chapter_extras` 未註冊）

重新啟動 Django 伺服器即可：
```bash
# 停止伺服器（Ctrl+C），然後重新啟動
python manage.py runserver
```

這是因為 Django 在啟動時才會載入模板標籤庫，新建立的 `templatetags` 模組需要重啟才能生效。

### 2. CSV 匯入失敗

- 確認 CSV 檔案使用 **逗號分隔**（非 Tab）
- 確認 CSV 檔案為 **UTF-8 編碼**（建議含 BOM，以便 Excel 正確開啟）
- 確認欄位名稱正確：`章節`, `題號`, `題目`, `選項A` ~ `選項E`, `正確答案`, `詳解`, `連貫題組別`, `自編題目`, `題目來源`

### 3. 圖片無法顯示

- 確認圖片檔案存放在 `quiz_app/static/quiz_app/images/` 目錄
- 確認圖片檔案名稱與資料庫中的路徑一致
- 執行 `python manage.py collectstatic` 收集靜態檔案

### 4. 資料庫遷移問題

```bash
# 清除所有遷移記錄，重新開始
python manage.py migrate quiz_app zero
python manage.py makemigrations
python manage.py migrate
```

---

## 授權

本專案為資料結構期末專題，僅供教育與學術用途。

---

## 開發者

- **CBF113007** 鄭書懷
- **CBF113018** 郭漢廷

*資料結構期末專題 — 宇宙深空主題測驗網站*
