from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware # 1. ADD THIS
import yt_dlp

app = FastAPI()

# 2. ADD THIS (This prevents the app from blocking your Flutter requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search(q: str = Query(...)):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extract_flat': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch5:{q}", download=False)
        return [{"title": x.get("title"), "url": x.get("url"), "thumb": x.get("thumbnail")} for x in info['entries']]

# 3. Vercel sometimes needs the app to be explicitly assigned to 'handler'
handler = app
