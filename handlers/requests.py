import httpx
from utils.etc import search_manga, get_chapter

# get manga chapters
def manga(url_query: str):
    return httpx.get(search_manga(url_query), timeout=None).json()


# chapter images getter
def chapter(url_query: str):
    return httpx.get(get_chapter(url_query), timeout=None).json()