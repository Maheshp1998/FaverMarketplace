import logging
import xml.etree.ElementTree as ET

import httpx
from httpx import HTTPStatusError, RequestError, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTTPXClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.Client(base_url=self.base_url, timeout=self.timeout)

    def _request(self, method: str, url: str, **kwargs) -> Response:
        try:
            response = self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except HTTPStatusError as exc:
            logger.error(
                f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}"
            )
            raise
        except RequestError as exc:
            logger.error(f"Request error occurred: {exc}")
            raise

    def get(self, url: str, **kwargs) -> Response:
        return self._request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        return self._request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> Response:
        return self._request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> Response:
        return self._request("DELETE", url, **kwargs)

    def close(self):
        self.client.close()

    def parse_xml(self, response: Response) -> ET.Element:
        events = []
        try:
            root = ET.fromstring(response.content)
            for base_event in root.findall(".//base_event"):
                base_event_data = {
                    "base_event_id": base_event.get("base_event_id"),
                    "sell_mode": base_event.get("sell_mode"),
                    "title": base_event.get("title"),
                    "events": [],
                }

                event_element = base_event.find("event")
                if event_element is not None:
                    event_data = {
                        "event_start_date": event_element.get("event_start_date"),
                        "event_end_date": event_element.get("event_end_date"),
                        "event_id": event_element.get("event_id"),
                        "sell_from": event_element.get("sell_from"),
                        "sell_to": event_element.get("sell_to"),
                        "sold_out": event_element.get("sold_out"),
                        "zones": [],
                    }

                    base_event_data["prices"] = [
                        float(zone.get("price", 0))
                        for zone in event_element.findall("zone")
                    ]
                    base_event_data.update(event_data)
                events.append(base_event_data)
            return events
        except ET.ParseError as e:
            logger.error(f"Failed to parse XML: {e}")
            raise
