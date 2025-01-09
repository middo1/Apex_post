import json
from pathlib import Path

class Page:
    def __init__(self, data: dict) -> None:
        self.message: str
        self.comment: str
        self.page_group: list[str] = data["page_group"]
        self.image_file: str = data['image_file']
        
        with open(data['message']) as msg_file:
            self.message = msg_file.read()

        with open(data["comment"]) as cmt_file:
            self.comment = cmt_file.read()

class ConfigParser:
    def __init__(self, path: Path) -> None:
        data: dict|None = None

        with open(path) as file:
            print(path, path.exists())
            data = json.load(file)

        if data is None:
            raise Exception("No data")

        self.access_token = data["access_token"]
        self.pages: list[Page] = [Page(d) for d in data["pages"]]