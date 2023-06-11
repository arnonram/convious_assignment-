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
        print("Getting restaurants")
        return self.request.get(f"{self.base_url}/restaurants/")

    def create_restaurant(self, name) -> requests.Response:
        print(f"Creating restaurant with name: {name}")
        payload = {"name": name}
        return self.request.post(f"{self.base_url}/restaurants/", json=payload)

    def update_restaurant(self, id, name) -> requests.Response:
        print(f"Updating restaurant with id: {id} and name: {name}")
        payload = {"name": name}
        return self.request.put(f"{self.base_url}/restaurants/{id}/", json=payload)

    def delete_restaurant(self, id) -> requests.Response:
        print(f"Deleting restaurant with id: {id}")
        return self.request.delete(f"{self.base_url}/restaurants/{id}/")
