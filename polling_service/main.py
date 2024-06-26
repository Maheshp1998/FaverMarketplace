import asyncio
import logging
import time
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from market_events.polling import PollEvents
from settings import POLL_TIMER

LOGGER = logging.getLogger(__name__)


async def poll(polling_class: PollEvents):
    while True:
        try:
            start_time = time.time()
            LOGGER.info("Polling events...")
            polling_class.poll()
            end_time = time.time()
            LOGGER.info(f"Polling completed in {(end_time - start_time):.2f} seconds")
        except Exception as err:
            LOGGER.error(f"Error polling events {err}")
        finally:
            LOGGER.info(f"Awaitng for {POLL_TIMER} seconds")
            await asyncio.sleep(POLL_TIMER)


async def events_polling_task():
    try:
        events_poll = PollEvents()
        await poll(events_poll)
    except Exception as err:
        LOGGER.error(f"Error initializing events poll {err}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(events_polling_task())
    yield


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    uvicorn.run(app=app, port=8001)
