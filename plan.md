# 全面重新設計計畫 — 運用 13 個 Taste-Skill 美感

## Context
使用者要求「運用所有 skill 美感，重新設計網站」。目前的 Aurora Glass 黑暗主題仍然有太多 AI 預設風格（紫藍漸層、流星雨、游標光暈、大量 emoji、Inter 字體）。現在要依照 taste-skill 的設計原則全面重新設計。

## 設計方向：Editorial Study
暖色調編輯式學習平台，極簡 + 高階字體對比 + 自然互動。

### 融合各 skill 核心原則
| Skill | 貢獻 |
|-------|------|
| **minimalist-ui** | 暖色單色調、高字體對比、flat card、無 emoji、無 glassmorphism |
| **high-end-visual-design** | 雙層卡片架構、spring physics、nested CTA、staggered reveals |
| **stitch-design-taste** | 創意 8 / 密度 4 / 變異 8 / 動態 6 設定 |
| **redesign-existing-projects** | 審計優先序（字體→顏色→互動→佈局） |
| **industrial-brutalist-ui** | 極端字體尺寸對比、monospace data |
| **design-taste-frontend** | Three Dials、anti-slop 規則 |

### 診斷：目前網站中的 AI 預設痕跡
| 問題 | 目前狀況 |
|------|---------|
| Inter 字體 | 正在使用（skill 全部禁止） |
| 紫藍 AI 漸層背景 | #0f0c29 → #302b63 |
| 大量 emoji | 每個頁面都有 🎯🔄🏆📝🌳★ 等 |
| 流星雨 + 游標光暈 | 典型 AI 炫技裝飾 |
| backdrop-filter glassmorphism | skill 禁止在大型區塊使用 blur |
| 雙層色相偏移陰影 | 違反極淡 shadow 規則 |
| Centered Hero | 違反高變異度非對稱規則 |
| 三欄 stats + pill badge | 通用元件無特色 |

### 新調色盤
```
Canvas  #F7F6F3  (暖白背景)
Surface #FFFFFF  (卡片)
Ink     #111111  (主要文字，非純黑)
Steel   #787774  (次要文字)
Border  #EAEAEA  (1px 結構線)
Accent  #3B82F6  (單一強調色，藍)
Success #346538  (深綠) + #EDF3EC (背景淺綠)
Error   #9F2F2D  (深紅) + #FDEBEC (背景淺紅)
```

### 字體系統
- Display/UI: **Geist** (拉丁) + **Noto Sans TC** (中文)
- Mono: **Geist Mono** (數據、計時器、分數)
- 全面禁止：Inter、Roboto、Open Sans

### 與現在的主要差異
| 元素 | 現在 (Aurora Glass) | 新設計 (Editorial Study) |
|------|---------------------|-------------------------|
| 背景 | 深紫藍漸層 #0f0c29→#302b63 | 暖白 #F7F6F3 |
| 卡片 | glassmorphism backdrop-blur | 純白 + 1px #EAEAEA 邊框 |
| 字體 | Inter + Noto Sans TC | Geist + Noto Sans TC + Geist Mono |
| Emoji | 大量使用 | 全面移除，改文字/SVG |
| 裝飾 | 流星雨 + 游標光暈 | 無裝飾，乾淨簡潔 |
| 陰影 | 雙層色相偏移 | opacity < 0.05 極淡 shadow |
| 按鈕 | 漸層背景 | 純色 #111111 或 outline |
| Hero | 居中標題 | 左對齊 editorial style |
| 圓角 | 多層級 (8/16/24px) | 統一 8px |

## 修改檔案

### 1. CSS 完全重寫
**檔案：** `quiz_app/static/quiz_app/css/style.css`

移除內容：
- 所有 glassmorphism（backdrop-filter、半透明卡片）
- 所有 ::before 內緣高光偽元素
- 流星雨動畫（.meteor 全部）
- 游標光暈（.cursor-glow 及相關 JS）
- 雙層陰影系統（改用極淡 shadow）
- 漸層按鈕背景（改純色）
- Inter 字體導入

新增內容：
- Geist 字體導入（Google Fonts 或 @font-face）
- 暖色調 CSS 變數
- flat card 系統（white bg + 1px border + 8px radius）
- 純色按鈕系統（#111111 fill 或 outline）
- 表格、表單、選項等對應更新
- spring physics 過渡曲線 `cubic-bezier(0.16, 1, 0.3, 1)`
- hover/active micro-interactions

### 2. 全部 13 個 Templates 更新

**通用修改（每個 template）：**
- 移除所有 emoji（改為純文字或 unicode 符號）
- 更新 header/footer 結構（左對齊導航）
- 移除 terminal 前綴（~/home、~/result 等）
- 移除 inline styles → class-based
- 按鈕移除 emoji 前綴
- Profile Modal 保持功能、更新樣式

**各模板重點：**
- `home.html` — 重新設計 Hero（左對齊）、Feature cards、Chapter grid
- `quiz.html` — 重新設計設定面板（segmented control + toggle）
- `take_quiz.html` — 重新設計雙欄佈局（題號卡 + 題目卡）
- `result.html` — 重新設計分數展示、詳解列表
- `admin_panel.html` — 重新設計側欄、表格、統計卡片、Modal
- `leaderboard.html` — 更新排行表格
- `quiz_records.html` — 更新紀錄列表
- `wrong_answers.html` — 更新錯題列表
- `wrong_answers_detail.html` — 更新詳情
- `login.html` / `register.html` — 更新 auth 表單
- `random_quiz_setup.html` / `review_wrong.html` — 更新設定頁

## 執行順序
1. **style.css** 完全重寫
2. **home.html** 首頁入口
3. **quiz.html → take_quiz.html → result.html** 測驗流程
4. **admin_panel.html** 管理後台
5. 其餘頁面（leaderboard、records、wrong_answers）
6. **login.html / register.html** auth 頁面

## 驗證方式
1. `python manage.py check` — 確保無 Django 錯誤
2. `python manage.py runserver` — 瀏覽所有頁面
3. 確認所有功能正常（按鈕、連結、表單、Modal）
4. 確認 responsive 在 768px / 1024px / 1440px 的表現