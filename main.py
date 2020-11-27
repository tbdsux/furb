from base64 import decode
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from typing import Optional
from fastapi.templating import Jinja2Templates

from furb.utils import requester, chapter_getter, grabber
from furb.etc import decode_base64

app = FastAPI()

# mount the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# templates directory
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def index(request: Request, url: str = Form(...)):
    resp = await requester(url)

    manga_title = resp["title"]
    results = resp["chapters"]

    return templates.TemplateResponse(
        "output.html",
        {"request": request, "query": url, "results": results, "manga": manga_title},
    )


@app.get("/get/q/{b64_str}")
async def generate_download(request: Request, b64_str: str):
    try:
        url = decode_base64(b64_str)
    except Exception:
        return None

    resp = await chapter_getter(url)
    download = await grabber(resp["title"], resp["images"], url)

    return templates.TemplateResponse(
        "generate.html",
        {
            "request": request,
            "url": url,
            "chapter": resp["title"],
            "link": download["data"]["file"]["url"]["short"],  # get the download link
        },
    )