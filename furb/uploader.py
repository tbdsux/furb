# MAIN UPLOADER HANDLER
import httpx
import os

# ANONFILES.COM HOSTING API
ANONFILES_API = "https://api.anonfiles.com/upload"
BAYFILES_API = "https://api.bayfiles.com/upload"


class Uploader:
    def __init__(self, file_path: str, filename: str) -> None:
        super().__init__()

        # set datas
        self.file_path = file_path
        self.file_name = filename

    # AnonFiles.com API Uploader
    def AnonFiles(self):
        files = {"file": (self.file_name, open(self.file_path, "rb"))}

        resp = httpx.post(ANONFILES_API, files=files, timeout=None).json()

        # remove the file
        try:
            os.remove(self.file_path)
        except Exception:
            pass

        return resp

    # BayFiles.com API Uploader
    def BayFiles(self):
        files = {"file": (self.file_name, open(self.file_path, "rb"))}

        resp = httpx.post(BAYFILES_API, files=files, timeout=None).json()

        # remove the file
        try:
            os.remove(self.file_path)
        except Exception:
            pass

        return resp