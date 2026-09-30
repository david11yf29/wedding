# David & Grace 電子喜帖

單頁式電子喜帖，手機優先設計（乾燥玫瑰配色）。內容從 JSON 讀取，照片放在 `assets/`，由一個小型 FastAPI 伺服器提供網頁。

## 頁面內容

1. **開場**：點「開啟喜帖」進入
2. **封面**：主視覺照片、新人英文名、日期
3. **邀請**：邀請文案、雙方家長與新人姓名
4. **日期**：月曆（標記當天）、開席／入席時間、倒數計時
5. **場地**：Google 地圖、複製地址、交通方式、停車資訊
6. **相簿**：6 張照片，點擊可放大
7. **結尾**：回到頂端、分享喜帖（手機原生分享，不支援時改為複製網址）

## 專案結構

```
index.html                # 網頁（HTML + CSS + JS 單檔）
input/inputDetailed.json  # 喜帖內容：名字、時間、地點、交通、停車、分享文字
assets/                   # 照片
  cover.jpg               # 封面（直式）
  gallery-1 ~ 6.jpg       # 相簿；第 3、6 張為橫式，其餘直式
  parking-map.jpg         # 停車位置圖（選用）
main.py                   # FastAPI 靜態伺服器，讀取 PORT 環境變數
requirements.txt
Dockerfile
```

## 修改內容

- **文字資料**：編輯 `input/inputDetailed.json`，每個欄位的格式說明在檔案最上方的 `_guide`。空字串會沿用預設值。
- **照片**：以相同檔名替換 `assets/` 裡的檔案。建議長邊約 1800px，以加快載入速度。
- **停車位置圖**：放入 `assets/parking-map.jpg`，並把 `hasParkingMap` 設為 `true`。
- **相簿張數與橫幅位置**：修改 `index.html` 中的 `GALLERY` 與 `WIDE_GALLERY_INDEXES`。

## 本機預覽

需要 Python 3.10 以上。

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python main.py
```

開啟 http://localhost:8000 。

## 部署

預計部署到 AI Builder Space（Koyeb），部署管理頁面：https://space.ai-builders.com/deployments

- 需要公開的 GitHub repo
- 單一程序、單一 port，並讀取 `PORT` 環境變數（`main.py` 已處理）
- API key 請放在環境變數，不要寫進 repo

## 參考

- 版面架構參考同事的電子喜帖：https://wedding-invitation.mouse31620.workers.dev/
