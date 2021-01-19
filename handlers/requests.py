import httpx
from utils.etc import search_manga, get_chapter

# get manga chapters
def manga(url_query: str):
    resp = httpx.get(search_manga(url_query), timeout=None)

    # the magna-api server returns `null` 
    # if there was a problem with the request
    # so, try to decode it
    # and parse no data, if there was a problem
    json_response = {}
    try:
        json_response = resp.json()
    except Exception:
        pass # do nothing

    # return the status code and json response
    return resp.status_code, json_response


# chapter images getter
def chapter(url_query: str):
    resp = httpx.get(get_chapter(url_query), timeout=None)

    # the magna-api server returns `null` 
    # if there was a problem with the request
    # so, try to decode it
    # and parse no data, if there was a problem
    json_response = {}
    try:
        json_response = resp.json()
    except Exception:
        pass # do nothing

    # return the status code and json response
    return resp.status_code, json_response