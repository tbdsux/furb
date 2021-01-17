from furb.cache import Cacher

# main caching handler
# this will store the data to the mongodb
def cacher(data: dict):
    cache = Cacher(
        request_url=data["request_url"],
        file_name=data["file_name"],
        title=data["title"],
        link=data["upload_link"],
        anonfile_id=data["anonfile_id"],
    )

    # cache it
    return cache.insert()


# cache checker
# it will check for similar datas
# stored in the mongodb
def check_file_cache(url: str):
    cache = Cacher(request_url=url)

    # return the check
    return cache.check()