from dotenv import load_dotenv

# load local.env
load_dotenv()

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from utils.etc import decode_base64
from utils.api import request_api
from handlers.requests import manga, chapter
from handlers.caching import cacher, check_file_cache
from handlers.uploading import upload_handler
from handlers.grab import grabber

app = FastAPI()

# setup cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,  # Allows credentials
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# base model for posting data
# to the /grab endpoint
class URL(BaseModel):
    url: str


# main index
@app.get("/")
async def index():
    return "Furb API - Backend Service"


# scraper api service checker and ensurer
@app.get("/api")
async def api(response: Response):
    if request_api():
        return "OK"

    # if scraper api is down
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return "Backend API is currently down. Please try again later."


# grabber > query chapters handler
@app.post("/grab")
async def index(req: URL, response: Response):
    # get the posted data from the basemodel
    status_code, resp = manga(req.url)

    ### CHECK FOR THE STATUS_CODE IF VALID / OK
    if status_code == 404:
        # return a 404 error
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"error": "404", "message": "Your request was not found."}
    elif status_code == 500:
        # return a 500 error
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": "500", "message": "Internal server error problem."}

    # return the response, 200
    return {
        "manga_title": resp["title"],
        "results": resp["chapters"],
        "source": resp["source"],
    }


# main downloader, this will
# > download the chapter
# > create a .pdf file from the images
# > upload the pdf to the file hosting
@app.get("/get/q/{b64_str}")
async def generate_download(b64_str: str, response: Response):
    # pre-define title and link
    title = ""
    link = ""

    # try to decode the url sent
    # it might be good to just use the url,
    # but this is to ensure that the request
    # should not be unnecessarily modified from
    # the frontend by the client
    # also, this is for url-safety
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
        status_code, resp = chapter(url)

        ### CHECK FOR THE STATUS_CODE IF VALID / OK
        if status_code == 404:
            # return a 404 error
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"error": "404", "message": "Your request was not found."}
        elif status_code == 500:
            # return a 500 error
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"error": "500", "message": "Internal server error problem."}

        # download the images and create pdf
        file, chapter_filename = await grabber(resp["title"], resp["images"], url)

        # upload it
        upload = upload_handler(file)

        if upload.status:
            # cache the download link in order to speedup future requests
            cache = cacher(
                data={
                    "request_url": url,
                    "file_name": chapter_filename,
                    "title": resp["title"],
                    "upload_link": upload.data.file.url.short,
                    "anonfile_id": upload.data.file.metadata.id,
                }
            )

            # retrieve cache response
            title = cache["title"]
            link = cache["link"]

        else:
            # if there was a problem with the upload, it will return code 500
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"code": 500, "url": url, "message": "Internal Server Error"}

    # 200 > response code,
    # return the acquired response
    return {
        "code": 200,
        "url": url,
        "message": "Ok!",
        "data": {"title": title, "link": link},
    }