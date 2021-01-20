import httpx
from utils.etc import BASE_API

# this will request the scraper api service
# and ensure that it is live and working
def request_api():
    try:
        # return a false if request has failed (not ok)
        if httpx.get(BASE_API).status_code != 200:
            return False
    except Exception:
        # if there was a problem with the request
        # httpx.ConnectError / https.ConnectTimeout
        # return false as is
        return False

    # otherwise, return true
    return True