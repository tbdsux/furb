import re
import httpx
from PIL import Image
from io import BytesIO
import grequests
import os
import img2pdf
import shutil

ANONFILES_API = "https://api.anonfiles.com/upload"

LIMIT = 3  # concurrent requests for grequests


class Furb:
    def __init__(self, name, chapter_images, url) -> None:
        # pdf file name
        self.chapter_name = f"{name}.pdf"

        # for downloading images
        self.to_download = chapter_images
        self.headers = {"Referer": url}  # some sites require this

        # temporary dir name
        self.temp_dir = "temp"

        self.images = []  # append images here

        # main working dir of the app
        self.main_working_dir = os.getcwd()

        # folder to store temp images downloaded
        self.folder_dir = os.path.join(self.main_working_dir, self.temp_dir, name)

        # path of the pdf file
        self.file = os.path.join(
            self.main_working_dir, self.temp_dir, self.chapter_name
        )

        self.upload_link = ""  # the upload link, ..

    # check if file already exists from the `temp` dir
    def file_checker(self):
        if os.path.exists(self.file):
            return True

        return False

    # Synchronous Grabber
    async def SyncGrabber(self):
        # download each, it may take some time
        for num, i in enumerate(self.to_download):
            await self.grab_image(num, i)

        # check if the files are downloaded to the folder name
        if len(os.listdir(self.folder_dir)) > 0:
            return True

    # download each image
    async def grab_image(self, count, img_url):
        async with httpx.AsyncClient() as client:
            resp = await client.get(img_url, timeout=None, headers=self.headers)

        try:
            os.makedirs(self.folder_dir)
        except Exception:
            pass

        os.chdir(self.folder_dir)

        fname = "{:03d}".format(count) + ".jpg"
        if not os.path.exists(os.path.join(self.folder_dir, fname)):
            # save each image
            try:
                raw_img = Image.open(BytesIO(resp.content)).convert("RGB")
                raw_img.save(
                    os.path.join(self.folder_dir, fname),
                    "jpeg",
                )
            except Exception:
                pass  # do nothing if there was a problem while trying to save the image

    # Multiple Grabber, Async [USE THIS IF YOUR SERVER HAS A RAM OF 500MB(maybe, 1GB) AND ABOVE]
    async def AsyncGrabber(self):
        rs = [grequests.get(i, headers=self.headers) for i in self.to_download]

        for i in grequests.map(rs, size=LIMIT):  # set the limit above
            self.images.append(Image.open(BytesIO(i.content)).convert("RGB"))

        if len(self.images) > 0:
            return True

    # make the temp_dir and ch to it
    def make_temp_dir(self):
        # make the folder
        try:
            os.mkdir(os.path.join(self.main_working_dir, self.temp_dir))
        except FileExistsError:
            pass

        os.chdir(os.path.join(self.main_working_dir, self.temp_dir))

    # for sorting images
    def sort_images(self, images):
        images = images
        images.sort(key=lambda f: int(re.sub("\D", "", f)))

        return images

    # direct from the list pdf maker
    async def Direct_PDFMaker(self):
        # set the dir
        self.make_temp_dir()

        # write pdf
        self.images[0].save(
            self.chapter_name,
            save_all=True,
            append_images=self.images[1:],
        )

        # reset the chdir
        os.chdir(self.main_working_dir)

    # make a pdf from a folder
    async def Folder_PDFMaker(self):
        # set the dir
        self.make_temp_dir()

        self.images = [
            os.path.join(self.folder_dir, i)
            for i in self.sort_images(
                [p for p in os.listdir(self.folder_dir) if p.endswith(".jpg")]
            )
        ]

        # some images can't be downloaded because missing, or external problems,
        # if there are no images found, do not continue
        if len(self.images) > 0:
            try:
                if not os.path.exists(self.file):
                    with open(self.file, "wb") as f:
                        f.write(img2pdf.convert(self.images))
            except Exception:
                pass

            # reset the chdir
            os.chdir(self.main_working_dir)

            # remove the downloaded files and dir
            shutil.rmtree(self.folder_dir, ignore_errors=True)

        return False

    # AnonFiles.com API Uploader
    async def Upload_to_AnonFiles(self):
        files = {"file": (self.chapter_name, open(self.file, "rb"))}

        async with httpx.AsyncClient() as client:
            resp = await client.post(ANONFILES_API, files=files, timeout=None)

        # remove the file
        try:
            os.remove(self.file)
        except Exception:
            pass

        return resp.json()
