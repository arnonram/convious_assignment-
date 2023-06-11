import json
import os
import requests
from api_clients.models.user_model import User


class UsersClient:
    def __init__(self):
        self.url_base = os.getenv("BASE_URL")
        self.api_version = os.getenv("API_VERSION")

        self.request = requests.Session()
        self.base_url = f"{self.url_base}{self.api_version}"
        self.request.headers.update({"Content-Type": "application/json"})
        self.request.headers.update(baseurl=self.base_url)

    def create_user(self, user):
        response = self.request.post(
            f"{self.base_url}/auth/users/create", data=json.dumps(user.__dict__)
        )

        if response.status_code == 201:
            print(f"User {user.username} created successfully")
        else:
            raise requests.exceptions.RequestException(
                f"Failed to create user {user.username} \n{response.text}"
            )

    def get_user_token(self, username: str, password: str) -> str:
        payload = {"username": username, "password": password}
        response = self.request.post(f"{self.base_url}/auth/token/login", json=payload)

        if response.status_code >= 200 and response.status_code < 300:
            print("User token generated successfully")
            return response.json()["auth_token"]
        else:
            raise requests.exceptions.RequestException(
                f"Failed to generate user token: {response.text}"
            )

    def authenticate_user(self, token):
        response = self.request.get(
            f"{self.base_url}/auth/users/me/", json={"token": token}
        )

        if response.status_code >= 200 and response.status_code < 300:
            print("User token verified successfully")
        else:
            raise requests.exceptions.RequestException(
                f"Failed to verify user token: {response.text}"
            )
