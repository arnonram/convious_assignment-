import os
import requests


class RestaurantsClient:
    def __init__(self, auth_token: str):
        self.url_base = os.getenv("BASE_URL")
        self.api_version = os.getenv("API_VERSION")

        self.request = requests.Session()
        self.base_url = f"{self.url_base}{self.api_version}"
        self.request.headers.update({"Content-Type": "application/json"})
        self.request.headers.update({"Authorization": f"Token {auth_token}"})

    def get_restaurants(self) -> requests.Response:
        return self.request.get(f"{self.base_url}/restaurants/")

    def create_restaurant(self, name) -> requests.Response:
        payload = {"name": name}
        return self.request.post(f"{self.base_url}/restaurants/", json=payload)

    def update_restaurant(self, id, name) -> requests.Response:
        payload = {"name": name}
        return self.request.put(f"{self.base_url}/restaurants/{id}/", json=payload)

    def delete_restaurant(self, id) -> requests.Response:
        return self.request.delete(f"{self.base_url}/restaurants/{id}/")
