# MAIN UPLOADER HANDLER
import httpx
import os

# ANONFILES.COM HOSTING API
ANONFILES_API = "https://api.anonfiles.com/upload"


class Uploader:
    def __init__(self, file_path, filename) -> None:
        super().__init__()
        # set datas
        self.file_path = file_path
        self.file_name = filename

    # AnonFiles.com API Uploader
    async def AnonFiles(self):
        files = {"file": (self.file_name, open(self.file_path, "rb"))}

        async with httpx.AsyncClient() as client:
            resp = await client.post(ANONFILES_API, files=files, timeout=None)

        # remove the file
        try:
            os.remove(self.file_path)
        except Exception:
            pass

        return resp.json()