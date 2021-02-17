import os
from furb.uploader import Uploader

# upload handler
# it will upload the *.pdf file to
# Anonfiles.com
def upload_handler(file, filename):
    upload = Uploader(file_path=file, filename=filename)

    # check env on what file hosting to use
    file_host = os.getenv("FILE_HOST")
    
    if file_host:
        if file_host.lower() == "bayfiles":
            # use bayfiles.com if set
            return upload.BayFiles()

    # upload it to anonfiles.com
    # this is the default if not set
    return upload.AnonFiles()
