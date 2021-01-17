from furb.furb import Furb

# main grabber / download handler
async def grabber(chapter: str, img_list: list, url: str):
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