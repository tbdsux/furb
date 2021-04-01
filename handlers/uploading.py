from __future__ import annotations

import os
from anonfiles import AnonFiles, BayFiles
from anonfiles.anonfiles import AnonErrorResponse, AnonSuccessResponse

# get the file hosting site to use
def get_file_host() -> AnonFiles | BayFiles:
    # check env on what file hosting to use
    file_host = os.getenv("FILE_HOST")

    # upload it to anonfiles.com
    # this is the default if not set
    u = AnonFiles()

    if file_host:
        if file_host.lower() == "bayfiles":
            # use bayfiles.com if set
            u = BayFiles()

    return u


# upload handler
# it will upload the *.pdf file to
# Anonfiles.com
def upload_handler(file: str) -> AnonSuccessResponse | AnonErrorResponse:
    u = get_file_host()

    # upload
    resp = u.upload(file=file)

    # remove file
    try:
        os.remove(file)
    except Exception:
        pass

    # return object response instance
    return resp
