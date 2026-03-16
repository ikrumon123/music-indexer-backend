from fastapi import FastAPI, Query
import yt_dlp

app = FastAPI()

@app.get("/search")
def search(q: str = Query(...)):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'extract_flat': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Searches YouTube and gets 5 results
        info = ydl.extract_info(f"ytsearch5:{q}", download=False)
        return [{"title": x.get("title"), "url": x.get("url"), "thumb": x.get("thumbnail")} for x in info['entries']]