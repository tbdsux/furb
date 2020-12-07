# MAIN FURB HANDLERS

from gevent import monkey as curious_george

# this is for the grequests
curious_george.patch_all(thread=False, select=False)

import httpx
from furb.etc import search_manga, get_chapter
from furb.furb import Furb
from furb.cache import Cacher
from furb.uploader import Uploader

# get manga chapters
async def requester(url_query):
    resp = ""
    async with httpx.AsyncClient() as client:
        resp = await client.get(search_manga(url_query), timeout=None)

    return resp.json()


# chapter images getter
async def chapter_getter(url_query):
    resp = ""
    async with httpx.AsyncClient() as client:
        resp = await client.get(get_chapter(url_query), timeout=None)

    return resp.json()


# main grabber / download handler
async def grabber(chapter, img_list, url):
    session = Furb(name=chapter, chapter_images=img_list, url=url)

    # check if file exists
    if not session.file_checker():
        grab = await session.SyncGrabber()

        if grab:
            # write pdf
            file = await session.Folder_PDFMaker()

            # return the file path
            return file, session.chapter_name

    # return the path of the file if it already exists
    return session.file, session.chapter_name


# upload handler
async def upload_handler(file, filename):
    upload = Uploader(file_path=file, filename=filename)

    # upload it to anonfiles.com
    return await upload.AnonFiles()


# cache checker
async def check_file_cache(request_url):
    cache = Cacher(request_url=request_url)

    # return it
    return await cache.check()


# caching handler
async def cacher(request_url, file_name, title, upload_link, anonfile_id):
    cache = Cacher(
        request_url=request_url,
        file_name=file_name,
        title=title,
        link=upload_link,
        anonfile_id=anonfile_id,
    )

    # cache it
    return await cache.insert()
