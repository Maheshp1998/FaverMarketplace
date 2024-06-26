import logging

from settings import API_BASE_URL, BACKEND_API_BASE_URL

from .backend_client import BackendClient
from .events_client import EventsClient


class PollEvents:
    client: EventsClient
    backend_client: BackendClient
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.logger.info("Initializing events polling")
        self.base_url = API_BASE_URL
        self.backend_base_url = BACKEND_API_BASE_URL
        self.client = EventsClient(self.base_url)
        self.backend_client = BackendClient(self.backend_base_url)

        self.logger.info("Events polling initialized")

    def format_events(self, event: dict):
        event_payload = {
            "base_event_id": event.get("base_event_id"),
            "event_id": event.get("event_id"),
            "title": event.get("title"),
            "start_date_time": event.get("event_start_date"),
            "end_date_time": event.get("event_end_date"),
            "min_price": min(event.get("prices"), [0]),
            "max_price": max(event.get("prices"), [0]),
        }
        return event_payload

    def inject_event(self, event_data: dict):
        formatted_event = self.format_events(event_data)
        return self.backend_client.add_event(formatted_event)

    def filter_processed_events(self, events):
        unprocessed_events = []
        processed_ids = self.backend_client.get_processed_event_ids().json()
        for event in events:
            base_event_id = event.get("base_event_id")
            event_id = event.get("event_id")
            unique_id = f"{base_event_id}:{event_id}"
            if unique_id not in processed_ids:
                unprocessed_events.append(event)
                self.logger.info(f"Found unprocessed event: {unique_id}")
            else:
                self.logger.info(f"Event {unique_id} is already processed.")
        return unprocessed_events

    def poll(self):
        events = self.client.get_events()
        unprocessed_events = self.filter_processed_events(events=events)
        processed_count = 0
        for event in unprocessed_events:
            if event.get("sell_mode") == "online":
                self.inject_event(event_data=event)
                processed_count += 1
            else:
                base_event_id = event.get("base_event_id")
                event_id = event.get("event_id")
                self.logger.info(
                    f"Ignoring offline event with base event id {base_event_id} and event id {event_id}"
                )

        self.logger.info(f"Processed {processed_count} events")
