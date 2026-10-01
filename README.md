# David & Grace 電子喜帖

單頁式電子喜帖，手機優先設計：灰白底配淡玫瑰點綴、圓體字。內容從 JSON 讀取，照片放在 `assets/`，由一個小型 FastAPI 伺服器提供網頁。

## 頁面內容

1. **開場**：點「開啟喜帖」進入
2. **封面**：主視覺照片、白色細框、新人英文名、日期
3. **邀請**：邀請文案、雙方家長（框外）與新郎／新娘（框內）
4. **日期**：月曆（標記當天）、開席／入席時間、倒數計時
5. **場地**：場地照片標題、Google 地圖、複製地址、如何前往、行車路線、停車資訊
6. **相簿**：6 張照片，點擊可放大
7. **結尾**：回到頂端、分享喜帖（手機原生分享，不支援時改為複製網址）

從第二個區塊開始，捲動到該區時內容會逐一由下往上進入；手機開啟「減少動態效果」時則直接顯示。

## 專案結構

```
index.html                # 網頁（HTML + CSS + JS 單檔）
input/inputDetailed.json  # 喜帖內容：名字、時間、地點、交通、行車、停車、分享文字
assets/                   # 照片（會公開在 repo 上）
  cover.jpg               # 封面（直式）
  gallery-1 ~ 6.jpg       # 相簿；第 3、6 張為橫式，其餘直式
  venue.jpg               # 「婚禮場地」標題的背景照片（橫式）
  parking-map.jpg         # 停車位置圖（選用，目前未使用）
main.py                   # FastAPI 靜態伺服器，提供 / 、/assets、/input，讀取 PORT 環境變數
requirements.txt
Dockerfile
```

只存在本機、不會上傳的資料夾（見 `.gitignore`）：

- `originals/`：原尺寸照片備份
- `.venv/`：Python 虛擬環境

## 修改內容

### 文字資料

編輯 `input/inputDetailed.json`，存檔後重新整理頁面即可。每個欄位的格式說明在檔案最上方的 `_guide`。

| 欄位 | 說明 |
|---|---|
| `weddingDate` | 開席日期時間，例：`2026-12-12T12:00`（視為台灣時間） |
| `seatingTime` | 入席時間，例：`11:30 AM` |
| `groom` / `bride` | `en` 英文名、`zh` 中文名、`parents` 家長姓名 |
| `message` | 邀請文案，留空則使用預設文案 |
| `venue` | 場地名稱、樓層、地址、Google Maps 連結 |
| `transport` / `driving` / `parking` | 交通、行車路線、停車資訊，每筆有 `title` 與 `detail`；留 `[]` 則隱藏該區塊 |
| `hasParkingMap` | 有 `assets/parking-map.jpg` 時設為 `true` |
| `share` | 分享喜帖時帶出的標題與文字 |

注意 JSON 格式：字串要用雙引號、項目之間要有逗號、最後一項後面不能有逗號。格式錯誤時頁面會改用預設內容，可在瀏覽器主控台看到警告。

### 照片

- 以相同檔名替換 `assets/` 裡的檔案。建議長邊約 1800px，以加快載入速度；原圖可放在 `originals/` 備份。
- **相簿張數與橫幅位置**：修改 `index.html` 中的 `GALLERY` 與 `WIDE_GALLERY_INDEXES`。

### 配色與字體

都在 `index.html` 開頭的 `:root`：

| 變數 | 目前值 | 用途 |
|---|---|---|
| `--paper` | `#ffffff`（白色一） | 卡片：新郎／新娘、倒數、資訊卡片 |
| `--paper-2` | `#f8f9f7` | 所有區塊與結尾的背景 |
| `--page-bg` | `#f3f4f2` | 電腦寬螢幕上頁面兩側 |
| `--accent` | `#c8a3a7` | 淡玫瑰：月曆當天圓圈等大面積點綴 |
| `--accent-dark` | `#a8737b` | 深一階玫瑰：英文小標題、按鈕、新人名字 |
| `--ink` | `#4a3036` | 主要文字 |

字體：新人英文名用 Cormorant Garamond（`--display`），其餘英文與數字用 Quicksand，中文用粉圓體 Huninn。

## 本機預覽

需要 Python 3.10 以上。

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

開啟 http://localhost:8000 。改完看不到變化時，按 Cmd+Shift+R 強制重新載入。

**用手機預覽**：手機與 Mac 連同一個 Wi-Fi，開啟 `http://<Mac 的 IP>:8000`。Mac 的 IP 可用以下指令查詢：

```bash
ipconfig getifaddr en0
```

打不開時，檢查 Mac 防火牆是否允許 Python 接受連線。

也可以用 Docker 執行：

```bash
docker build -t wedding . && docker run --rm -p 8000:8000 wedding
```

## 修改流程

1. 從 `main` 開新分支修改
2. 推上 GitHub 並開 PR 合併回 `main`
3. 合併後在本機更新：

```bash
git checkout main && git pull
```

## 部署

預計部署到 AI Builder Space（Koyeb），部署管理頁面：https://space.ai-builders.com/deployments

- 需要公開的 GitHub repo；照片、姓名、地址都會公開
- 單一程序、單一 port，並讀取 `PORT` 環境變數（`main.py` 已處理，預設 8000）
- API key 請放在環境變數（例如 `AI_BUILDER_API_KEY`），不要寫進 repo
- 部署參數：`repo_url`（`https://github.com/david11yf29/wedding`）、`service_name`（即子網域，小寫英數與 `-`，3–32 字元）、`branch`（`main`）、`port`（`8000`）
- `repo_url` 在第一次部署後會綁定 `service_name`，之後不能更換
- 部署為非同步，約 5–10 分鐘，狀態變成 `HEALTHY` 即完成

## 參考

- 版面架構參考同事的電子喜帖：https://wedding-invitation.mouse31620.workers.dev/
- AI Builder API 文件：https://www.ai-builders.com/resources/students-backend/openapi.json
