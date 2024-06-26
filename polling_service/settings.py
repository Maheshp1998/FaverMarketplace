from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_base_url: str = Field(
        "https://gist.githubusercontent.com/sergio-nespral/82879974d30ddbdc47989c34c8b2b5ed/raw/44785ca73a62694583eb3efa0757db3c1e5292b1/response_2.xml",
        description="The base url of the event market place API",
    )
    backend_api_base_url: str = Field(
        "http://127.0.0.1:8000",
        description="The base url of backend",
    )
    poll_timer: int = Field(
        30,
        description="Poll time to fetch data from market events api",
    )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

API_BASE_URL = settings.api_base_url
BACKEND_API_BASE_URL = settings.backend_api_base_url
POLL_TIMER = settings.poll_timer
