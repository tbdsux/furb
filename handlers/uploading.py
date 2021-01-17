from furb.uploader import Uploader

# upload handler
# it will upload the *.pdf file to
# Anonfiles.com
def upload_handler(file, filename):
    upload = Uploader(file_path=file, filename=filename)

    # upload it to anonfiles.com
    return upload.AnonFiles()
