import re
import httpx
from PIL import Image
from io import BytesIO
import os
import img2pdf
import shutil

LIMIT = 3  # concurrent requests for grequests


class Furb:
    def __init__(self, name: str, chapter_images: list, url: str) -> None:
        # pdf file name
        self.chapter_name = f"{name}.pdf"

        # for downloading images
        self.to_download = chapter_images
        self.headers = {"Referer": url}  # some sites require this

        # temporary dir name
        self.temp_dir = "temp"

        # append images here
        self.images = []

        # main working dir of the app
        self.main_working_dir = os.getcwd()

        # folder to store temp images downloaded
        self.folder_dir = os.path.join(self.main_working_dir, self.temp_dir, name)

        # path of the pdf file
        self.file = os.path.join(
            self.main_working_dir, self.temp_dir, self.chapter_name
        )

        # the upload link, ..
        self.upload_link = ""

    # check if file already exists from the `temp` dir
    def file_checker(self):
        if os.path.exists(self.file):
            return True

        return False

    # Synchronous Grabber
    # asyncio will be implemented in the future
    async def SyncGrabber(self):
        # download each, it may take some time
        async with httpx.AsyncClient() as client:
            for num, i in enumerate(self.to_download):
                await self.grab_image(num, i, client)

        # check if the files are downloaded to the folder name
        # the number of images downloaded should be equal
        # to the images that are queued to be downloadede
        if len(os.listdir(self.folder_dir)) == len(self.to_download):
            return True

        # else,
        return False

    # download each image
    async def grab_image(self, count: int, img_url: str, client: httpx.AsyncClient):
        # ensure current working directory
        # this is to avoid saving the images
        # to different dirs
        try:
            os.makedirs(self.folder_dir)
        except Exception:
            pass
        os.chdir(self.folder_dir)

        # download image
        resp = await client.get(img_url, timeout=None, headers=self.headers)

        # save image
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

    # make the temp_dir and ch to it
    def make_temp_dir(self):
        # make the folder
        try:
            os.mkdir(os.path.join(self.main_working_dir, self.temp_dir))
        except FileExistsError:
            pass

        os.chdir(os.path.join(self.main_working_dir, self.temp_dir))

    # for sorting images
    def sort_images(self, images: list):
        images = images
        images.sort(key=lambda f: int(re.sub("\D", "", f)))

        return images

    # direct from the list pdf maker
    # use this only if server is bigger (maybe 2gb ram up?)
    # this will crash the api on low-end servers
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

        # append sorted images with the folder dir
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

            # return the file path
            return self.file

        return False
