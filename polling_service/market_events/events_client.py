from settings import API_BASE_URL

from .client import HTTPXClient

BASE_URL = API_BASE_URL


class EventsClient(HTTPXClient):

    def __init__(self, base_url: str = BASE_URL, timeout: int = 10):
        super().__init__(base_url, timeout)

    def get_events(self):
        return self.parse_xml(self.get("/"))
