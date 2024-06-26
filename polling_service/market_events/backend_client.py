from settings import BACKEND_API_BASE_URL

from .client import HTTPXClient

BASE_URL = BACKEND_API_BASE_URL


class BackendClient(HTTPXClient):

    def __init__(self, base_url: str = BASE_URL, timeout: int = 10):
        super().__init__(base_url, timeout)

    def get_events(self):
        return self.get("/api/events/").json()

    def add_event(self, payload: dict):
        return self.post("/api/events/", data=payload)

    def get_processed_event_ids(self):
        return self.get("/api/events/backend/ids")
