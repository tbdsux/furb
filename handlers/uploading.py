import os
from furb.uploader import Uploader

# upload handler
# it will upload the *.pdf file to
# Anonfiles.com
def upload_handler(file, filename):
    upload = Uploader(file_path=file, filename=filename)

    # check env on what file hosting to use
    # use bayfiles.com if set
    if os.getenv("FILE_HOST").lower() == "bayfiles":
        return upload.BayFiles()

    # upload it to anonfiles.com
    # this is the default if not set
    return upload.AnonFiles()
