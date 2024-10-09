from dotenv import load_dotenv
load_dotenv()

import secrets, os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from models import LongUrl, ShortUrl
from db import client


db = client()
app = FastAPI()


origins = []

web_url = os.environ.get("ZEUS_URL") # Frontend url
origins.append(web_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return "Zeus!!!! ⚡⚡⚡"

@app.get("/{custom}")
async def redirect(request: Request, custom: str):
    data = db.table("urls").select("id, original_url, accessed_count").eq("short_code", custom).execute()
    print(data.data)

    if len(data.data) == 0:
        print("[-] URL doesn't exist")
        print("[-] Redirecting to index")
        return RedirectResponse(url=request.base_url)
    else:
        print("[+] URL exists")
        print("[+] Redirecting to URL")
        original_url = data.data[0]["original_url"]
        
        if not original_url.startswith("http://") and not original_url.startswith("https://"):
            if original_url.startswith("www."):
                scheme = request.url.scheme
                original_url = f"{scheme}://{original_url}"
            else:
                scheme = request.url.scheme
                original_url = f"{scheme}://www.{original_url}"

        count_url = data.data[0]["accessed_count"]
        id_url = data.data[0]["id"]
        db.table("urls").update({"accessed_count": count_url + 1}).eq("id", id_url).execute()

    print(original_url)
    return RedirectResponse(url=original_url)

@app.post("/api/urls/shorten", response_model=ShortUrl)
async def shorten(long: LongUrl, request: Request):
    print(f'long: {long.long_url}')
    data = db.table("urls").select("short_code").eq("original_url", long.long_url).execute()
    code = ""
    if data.data == []:
        print("[+] Generating custom URL")
        code = secrets.token_urlsafe(8)
        print("[+]", long.long_url, code)
        db.table("urls").insert({
            "original_url": long.long_url,
            "short_code": code,
            "accessed_count": 0
        }).execute()
    else:
        print("[-] URL already in db")
        code = data.data
        code = code[0]["short_code"]
    base_url = request.base_url
    url = str(base_url) + code
    return ShortUrl(short_url = url)

@app.get("/api/urls")
async def getAll():
    data = db.table("urls").select("*").execute()
    return data.data

