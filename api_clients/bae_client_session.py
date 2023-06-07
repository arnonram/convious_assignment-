import requests
import os
from dotenv import load_dotenv
from urllib.parse import urljoin


class BaseClientSession(requests.Session):
    def __init__(self):
        load_dotenv()
        super().__init__()
        self.url_base = os.getenv("BASE_URL")
        self.api_version = os.getenv("API_VERSION")
        if not self.url_base or not self.api_version:
            raise ValueError("BASE_URL or API_VERSION not set")
        if not self.url_base.startswith("http"):
            raise ValueError("url must start with http")
        self.url_base = urljoin(self.url_base, self.api_version)

    def request(self, url, *args, **kwargs):
        if not url:
            raise ValueError("url or method not set")

        url = urljoin(self.url_base, url)
        return super().request(
            url, headers={"Content-Type: application/json"}, *args, **kwargs
        )
