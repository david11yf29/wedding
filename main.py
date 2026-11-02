import os

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


# 網頁與 JSON 每次都向伺服器確認是否有新版（沒變時只回 304），避免手機瀏覽器顯示舊版
@app.middleware("http")
async def no_cache_pages(request, call_next):
    response = await call_next(request)
    if request.url.path == "/" or request.url.path.startswith("/input/"):
        response.headers["Cache-Control"] = "no-cache"
    return response


app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "assets")), name="assets")
app.mount("/input", StaticFiles(directory=os.path.join(BASE_DIR, "input")), name="input")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def index():
    return FileResponse(os.path.join(BASE_DIR, "index.html"))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8001")))
