# David & Grace 電子喜帖

單頁式電子喜帖，手機優先設計：灰白底配淡玫瑰點綴、圓體字。內容從 JSON 讀取，照片放在 `assets/`，由一個小型 FastAPI 伺服器提供網頁。

線上網址：https://wedding-invitation.ai-builders.space/

## 頁面內容

1. **開場**：點「開啟喜帖」進入；每次開啟都從封面開始（不會停在上次捲動的位置）
2. **封面**：主視覺照片、白色細框、新人英文名、日期；照片底部有深色漸層，讓文字清楚
3. **邀請**：邀請文案、雙方家長（框外）與新郎／新娘（框內）
4. **日期**：月曆（標記當天）、開席／入席時間、倒數計時
5. **場地**：場地照片標題、Google 地圖、複製地址、如何前往、行車路線、停車資訊
6. **相簿**：7 張照片（點擊可放大），下方是 YouTube 影片（16:9）與 YouTube Shorts（9:16），各有「在 YouTube 觀看」備用連結；影片捲到畫面中會靜音自動播放，滑走就暫停
7. **結尾**：回到頂端、分享喜帖（手機原生分享，不支援時改為複製網址）

從第二個區塊開始，捲動到該區時內容會逐一由下往上進入；手機開啟「減少動態效果」時則直接顯示。

## 專案結構

```
index.html                # 網頁（HTML + CSS + JS 單檔），含連結預覽用的 meta 標籤
input/inputDetailed.json  # 喜帖內容：名字、時間、地點、交通、行車、停車、分享文字
assets/                   # 照片（會公開在 repo 上）
  cover.jpg               # 封面（直式），也是連結預覽圖
  gallery-1 ~ 7.jpg       # 相簿
  venue.jpg               # 「婚禮場地」標題的背景照片（橫式）
  backup/                 # 被換掉的舊照片與原尺寸照片（隨機檔名）；在 repo 裡，但不會部署
main.py                   # FastAPI 伺服器：/ 、/assets、/input、/health，讀取 PORT 環境變數（預設 8001）
requirements.txt
Dockerfile
```

只存在本機、不會上傳的資料夾：

- `originals/`：原尺寸照片備份（`.gitignore`）
- `.venv/`：Python 虛擬環境（`.gitignore`）

`assets/backup/` 會上傳到 GitHub（公開），但列在 `.dockerignore`，不會包進部署，網站上也打不開。

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
| `hasParkingMap` | 有 `assets/parking-map.jpg` 時設為 `true`（目前沒有這張圖，設為 `false`） |
| `share` | 分享喜帖時帶出的標題與文字 |

注意 JSON 格式：字串要用雙引號、項目之間要有逗號、最後一項後面不能有逗號。格式錯誤時頁面會改用預設內容，可在瀏覽器主控台看到警告。

### 連結預覽（LINE、Messenger 等）

預覽不會執行 JS，所以不會讀 JSON。標題、描述、網址與預覽圖直接寫在 `index.html` 開頭的 `<meta>`（`og:title`、`og:description`、`og:url`、`og:image`）。改名字或網址時要一起改。

LINE、FB 會快取預覽，改完後可能要一段時間才會更新。

### 照片

- 以相同檔名替換 `assets/` 裡的檔案。建議長邊約 1800px，以加快載入速度；原圖可放在 `originals/` 或 `assets/backup/` 備份。
- **相簿張數與橫幅位置**：修改 `index.html` 中的 `GALLERY` 與 `WIDE_GALLERY_INDEXES`。目前第 3、6、7 張為橫幅（跨兩欄），其餘以直式比例裁切、兩兩一排。
- **相簿縮圖放大**：`index.html` 中的 `GALLERY_ZOOM`（依索引設定倍率），目前第 4 張放大 1.15 倍；只影響相簿縮圖，點開的大圖不受影響。
- **封面底部漸層**：`index.html` 中的 `.cover::after`。目前 0–40% 透明（保留臉部），往下逐漸加深到底部 0.96，用來遮住照片下方的桌子並讓文字清楚。換封面照片時可能需要調整。

### YouTube 影片

在 `index.html` 搜尋 `videoFrame`，兩個地方要一起改：

- `<iframe src="https://www.youtube.com/embed/影片ID">`：內嵌播放器
- 下方「在 YouTube 觀看」的連結：`https://www.youtube.com/watch?v=影片ID`。部分瀏覽器或外掛會擋 Referer，導致 YouTube 錯誤 153，這時用這個連結觀看

Shorts 在 `shortsFrame`，同樣兩處要一起改，備用連結格式是 `https://www.youtube.com/shorts/影片ID`。

每個 iframe 網址後面的 `?enablejsapi=1&mute=1&playsinline=1` 要保留，捲動自動播放需要它。外框加上 `js-autoplay-video` class 就會套用捲動播放。

影片框比例在 `.video-frame` 的 `aspect-ratio`：橫式 `16 / 9`；加上 `is-vertical` class 會變成直式 `9 / 16`、寬度上限 `320px`。

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

開啟 http://localhost:8001 。改完看不到變化時，按 Cmd+Shift+R 強制重新載入。

**用手機預覽**：手機與 Mac 連同一個 Wi-Fi，開啟 `http://<Mac 的 IP>:8001`。Mac 的 IP 可用以下指令查詢：

```bash
ipconfig getifaddr en0
```

打不開時，檢查 Mac 防火牆是否允許 Python 接受連線。

也可以用 Docker 執行：

```bash
docker build -t wedding . && docker run --rm -p 8001:8001 wedding
```

## 修改流程

1. 從 `main` 開新分支修改
2. 推上 GitHub 並開 PR 合併回 `main`
3. 合併後在本機更新：

```bash
git checkout main && git pull
```

4. 重新部署（見下方）。合併到 `main` **不會**自動部署

## 部署

部署在 AI Builder Space（Koyeb），從 GitHub 的 `main` 分支建置。部署管理頁面：https://space.ai-builders.com/deployments （只能查看狀態，沒有重新部署按鈕）

| 參數 | 值 |
|---|---|
| `repo_url` | `https://github.com/david11yf29/wedding`（已綁定 `service_name`，不能更換） |
| `service_name` | `wedding-invitation`（即子網域） |
| `branch` | `main` |
| `port` | `8001` |

重新部署要用 API 金鑰（在 AI Builder Space 的 Settings 產生）。金鑰放在環境變數 `AI_BUILDER_API_KEY`，不要寫進 repo，也不要貼到聊天或文件裡。

```bash
curl -X POST "https://space.ai-builders.com/backend/v1/deployments" -H "Authorization: Bearer $AI_BUILDER_API_KEY" -H "Content-Type: application/json" -d '{"repo_url":"https://github.com/david11yf29/wedding","service_name":"wedding-invitation","branch":"main","port":8001}'
```

回應 `202` 且狀態為 `queued` 即已排入。查看進度（`queued` → `deploying` → `HEALTHY`）：

```bash
curl -s -H "Authorization: Bearer $AI_BUILDER_API_KEY" "https://space.ai-builders.com/backend/v1/deployments/wedding-invitation"
```

- 實際約 1 分鐘就會變成 `HEALTHY`
- 需要公開的 GitHub repo；照片、姓名、地址都會公開（網頁有 `noindex`，不會被搜尋引擎收錄）
- 單一程序、單一 port，並讀取 `PORT` 環境變數
- 每位使用者最多 2 個服務；免費託管至 2027-10-19

## 參考

- 版面架構參考同事的電子喜帖：https://wedding-invitation.mouse31620.workers.dev/
- AI Builder API 文件：https://www.ai-builders.com/resources/students-backend/openapi.json
- 部署到 AI Builder：https://space.ai-builders.com/deployments 