from gevent import monkey as curious_george

curious_george.patch_all(thread=False, select=False)

import httpx
from furb.etc import search_manga, get_chapter
from furb.furb import Furb


async def requester(url_query):
    resp = ""
    async with httpx.AsyncClient() as client:
        resp = await client.get(search_manga(url_query), timeout=None)

    return resp.json()


async def chapter_getter(url_query):
    resp = ""
    async with httpx.AsyncClient() as client:
        resp = await client.get(get_chapter(url_query), timeout=None)

    return resp.json()


async def grabber(chapter, img_list, url):
    session = Furb(name=chapter, chapter_images=img_list, url=url)

    # check if file exists
    if not session.file_checker():
        grab = await session.AsyncGrabber()

        if grab:
            # write pdf
            await session.PDFMaker()

    # upload to anonfiles.com
    upload = await session.Upload_to_AnonFiles()

    return upload