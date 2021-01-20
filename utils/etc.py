# Somewhat a CONFIG File

import base64


BASE_API = "https://magna-sc.com/"
CHAPTERS = "chapters"
MANGA = "manga"
QUERY = "?q="

# search parameter
def search_manga(query):
    return BASE_API + MANGA + QUERY + query


# chapter images paramter
def get_chapter(query):
    return BASE_API + MANGA + "/" + CHAPTERS + QUERY + query


# decode base64 encoding
def decode_base64(str):
    return base64.b64decode(str.encode("ascii")).decode("ascii")