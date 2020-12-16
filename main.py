from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from furb.handlers import (
    requester,
    chapter_getter,
    grabber,
    cacher,
    check_file_cache,
    upload_handler,
)
from furb.etc import decode_base64
import json

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
    source = resp['source']

    return templates.TemplateResponse(
        "output.html",
        {"request": request, "query": url, "results": results, "manga": manga_title, "source": source},
    )


@app.post("/get/q/{b64_str}")
async def generate_download(request: Request, b64_str: str):
    title = ""
    link = ""

    try:
        url = decode_base64(b64_str)
    except Exception:
        return {"code": 428, "message": "Precondition Required"}

    # check if the cache exists or nots
    check = await check_file_cache(url)
    if check:
        title = check["title"]
        link = check["link"]
    else:
        # download the chapter
        resp = await chapter_getter(url)
        file, chapter_filename = await grabber(resp["title"], resp["images"], url)

        # upload it
        upload = await upload_handler(file, chapter_filename)

        if upload["status"]:
            # cache the download link in order to speedup future requests
            cache = await cacher(
                request_url=url,
                file_name=chapter_filename,
                title=resp["title"],
                upload_link=upload["data"]["file"]["url"]["short"],
                anonfile_id=upload["data"]["file"]["metadata"]["id"],
            )
            title = cache["title"]
            link = cache["link"]

        else:
            # if there was a problem with the upload, it will return code 500
            return {"code": 500, "url": url, "message": "Internal Server Error"}

    return {
        "code": 200,
        "url": url,
        "message": "Ok!",
        "data": {"title": title, "link": link},
    }


@app.get("/download/q/{b64_str}")
async def download(request: Request, b64_str: str):
    try:
        resp = json.loads(decode_base64(b64_str))
    except Exception:
        return None  # return null if there was a problem while decoding

    title = resp['title']
    link = resp['dl_link']

    return templates.TemplateResponse(
        "generate.html",
        {
            "request": request,
            "chapter": title,
            "link": link,  # get the download link
        },
    )