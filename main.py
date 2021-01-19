from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from utils.etc import decode_base64
from handlers.requests import manga, chapter
from handlers.caching import cacher, check_file_cache
from handlers.uploading import upload_handler
from handlers.grab import grabber

app = FastAPI()

# setup cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True, # Allows credentials
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# base model for posting data
# to the /grab endpoint
class URL(BaseModel):
    url: str


@app.get("/")
async def index():
    return "Furb API - Backend Service"


@app.post("/grab")
async def index(req: URL):
    resp = manga(req.url)

    manga_title = resp["title"]
    results = resp["chapters"]
    source = resp["source"]

    return {"manga_title": manga_title, "results": results, "source": source}


@app.get("/get/q/{b64_str}")
async def generate_download(b64_str: str, response: Response):
    title = ""
    link = ""

    try:
        url = decode_base64(b64_str)
    except Exception:
        # this means there was a problem decoding the base64 string
        # return HTTP 428, is base-64 is modified from url
        response.status_code = status.HTTP_428_PRECONDITION_REQUIRED
        return {"code": 428, "message": "Precondition Required"}

    # check if the cache exists or nots
    check = check_file_cache(url)
    if check:
        title = check["title"]
        link = check["link"]
    else:
        # get the chapter
        resp = chapter(url)

        # download the images and create pdf
        file, chapter_filename = await grabber(resp["title"], resp["images"], url)

        # upload it
        upload = upload_handler(file, chapter_filename)

        if upload["status"]:
            # cache the download link in order to speedup future requests
            cache = cacher(
                data={
                    "request_url": url,
                    "file_name": chapter_filename,
                    "title": resp["title"],
                    "upload_link": upload["data"]["file"]["url"]["short"],
                    "anonfile_id": upload["data"]["file"]["metadata"]["id"],
                }
            )

            # retrieve cache response
            title = cache["title"]
            link = cache["link"]

        else:
            # if there was a problem with the upload, it will return code 500
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"code": 500, "url": url, "message": "Internal Server Error"}

    return {
        "code": 200,
        "url": url,
        "message": "Ok!",
        "data": {"title": title, "link": link},
    }