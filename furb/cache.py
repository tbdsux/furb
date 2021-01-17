from dotenv import load_dotenv

# load local.env
load_dotenv()

import os
import pymongo
import httpx
from datetime import datetime


## UPDATE THESE VARS WITH YOUR DB INFO
DB_NAME = "Furb"
COLLECTIONS_NAME = "CurrentLinks"


class Cacher:
    # Initialize a new caching object.
    # request_url is required as default...
    def __init__(
        self,
        request_url: str,
        file_name: str = None,
        title: str = None,
        link: str = None,
        anonfile_id: str = None,
    ) -> None:
        super().__init__()

        self.ANONFILES_CHECKER_API = "https://api.anonfiles.com/v2/file/<ID>/info"

        # set the database
        client = pymongo.MongoClient(os.getenv("MONGO_DB"))
        db = client[DB_NAME]
        self.collection = db[COLLECTIONS_NAME]

        # set the data
        self.request_url = request_url
        self.file_name = file_name
        self.link = link
        self.title = title
        self.anonfile_id = anonfile_id

    # check if the data exists
    def check(self):
        data = self.collection.find_one({"request": self.request_url})
        if data:
            resp = httpx.get(
                self.ANONFILES_CHECKER_API.replace("<ID>", data["data"]["anonfile_id"]),
                timeout=None,
            ).json()

            # if the response is true, return the data
            if resp["status"]:
                return data["data"]

            # remove existing cached if it is false,
            # FALSE means that the file is removed from the hosting or is no longer available
            self.collection.delete_one({"request_url": self.request_url})

        # return false if files has been removed
        # or deleted from the file hosting
        return False

    # insert the data to the db
    def insert(self):
        data = {
            "request": self.request_url,
            "data": {
                "cache_date": datetime.utcnow(),
                "cached": True,
                "request": self.request_url,
                "title": self.title,
                "filename": self.file_name,
                "anonfile_id": self.anonfile_id,
                "link": self.link,
            },
        }

        self.collection.insert_one(data)

        # return the data
        return data["data"]