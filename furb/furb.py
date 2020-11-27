import httpx
from PIL import Image
from io import BytesIO
import grequests
import os

ANONFILES_API = "https://api.anonfiles.com/upload"

LIMIT = 3  # concurrent requests for grequests


class Furb:
    def __init__(self, name, chapter_images, url) -> None:
        self.chapter_name = f"{name}.pdf"
        self.to_download = chapter_images
        self.images = []
        self.temp_dir = "temp"
        self.headers = {"Referer": url}
        self.main_working_dir = os.getcwd()
        self.file = os.path.join(
            self.main_working_dir, self.temp_dir, self.chapter_name
        )

        self.upload_link = ""

    # check if file already exists from the `temp` dir
    def file_checker(self):
        if os.path.exists(self.file):
            return True

        return False

    # Synchronous Grabber
    async def SyncGrabber(self):
        # download each, it may take some time
        ##### THIS WILL BE CHANGED TO ASYNCIO BUT THE FILES NEED TO BE IN ORDER FOR THE PDF
        for i in self.to_download:
            await self.grab_image(i)

        if len(self.images) > 0:
            return True

    # Multiple Grabber, Async
    async def AsyncGrabber(self):
        rs = [grequests.get(i, headers=self.headers) for i in self.to_download]

        for i in grequests.map(rs, size=LIMIT):
            self.images.append(Image.open(BytesIO(i.content)).convert("RGB"))

        if len(self.images) > 0:
            return True

    # download each image
    async def grab_image(self, img_url):
        async with httpx.AsyncClient() as client:
            resp = client.get(img_url, timeout=None)

        # append to images
        self.images.append(Image.open(BytesIO(resp.content)).convert("RGB"))

    # pdf maker
    async def PDFMaker(self):
        # make the folder
        os.mkdir(self.temp_dir)
        os.chdir(self.temp_dir)

        # write pdf
        self.images[0].save(
            self.chapter_name,
            save_all=True,
            append_images=self.images[1:],
        )

        # reset the chdir
        os.chdir(self.main_working_dir)

    # AnonFiles.com API Uploader
    async def Upload_to_AnonFiles(self):
        files = {"file": (self.chapter_name, open(self.file, "rb"))}

        async with httpx.AsyncClient() as client:
            resp = await client.post(ANONFILES_API, files=files, timeout=None)

        return resp.json()
