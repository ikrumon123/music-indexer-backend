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
def search(q: str = Query(...)):
    # Optimized options for speed on Serverless
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist',  # Faster metadata extraction
        'skip_download': True,
        'nocheckcertificate': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # We search specifically for YouTube Music (ytmsearch) for better indexing
            info = ydl.extract_info(f"ytmsearch5:{q}", download=False)
            entries = info.get('entries', [])
            
            return [
                {
                    "title": x.get("title"), 
                    "url": x.get("url"), 
                    "thumb": x.get("thumbnail"),
                    "id": x.get("id")
                } for x in entries if x is not None
            ]
    except Exception as e:
        # Returning the error as JSON stops the "500 Internal Error" screen 
        # and tells you exactly what went wrong.
        return {"error": str(e)}
