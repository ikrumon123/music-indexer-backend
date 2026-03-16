from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vercel needs this to handle the request properly
@app.get("/")
def read_root():
    return {"status": "Indexer Active"}

@app.get("/search")
def search(q: str = Query(...)):
    # Minimalist options to prevent Vercel "Invocation Failed"
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True, # This is the most important for serverless
        'skip_download': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Using standard ytsearch to ensure compatibility
            search_results = ydl.extract_info(f"ytsearch5:{q}", download=False)
            
            if not search_results or 'entries' not in search_results:
                return {"results": []}

            output = []
            for entry in search_results['entries']:
                if entry:
                    output.append({
                        "title": entry.get("title"),
                        "url": entry.get("url"),
                        "thumb": entry.get("thumbnail"),
                        "id": entry.get("id")
                    })
            return {"results": output}
            
    except Exception as e:
        # This will show the actual error in the JSON instead of a 500 page
        return {"error": str(e)}

# Mandatory for Vercel Python Runtime
handler = app
