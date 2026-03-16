from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search_music(q: str = Query(...)):
    # These options are based on the latest yt-dlp documentation
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # CRITICAL for speed; only gets metadata
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # We use ytsearch: to ensure the scraper knows we are searching
            search_query = f"ytsearch10:{q}" 
            info = ydl.extract_info(search_query, download=False)
            
            if 'entries' not in info:
                return {"results": []}

            results = []
            for entry in info['entries']:
                if entry:
                    results.append({
                        "id": entry.get("id"),
                        "title": entry.get("title"),
                        "uploader": entry.get("uploader"),
                        "duration": entry.get("duration"),
                        "thumbnail": entry.get("thumbnail"),
                        "url": entry.get("url"), # The stream URL for your player
                    })
            
            return {"results": results}
            
    except Exception as e:
        return {"error": str(e)}

handler = app
