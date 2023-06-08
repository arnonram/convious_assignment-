import requests
from models.user import User
from api_clients.bae_client_session import BaseClientSession


class UsersClient:
    def __init__(self):
        self.session = BaseClientSession()

    def create_user(self, user: User):
        response = self.session.post("/auth/users/create", json=User)

        if response.status_code >= 200 and response.status_code < 300:
            print(f"User {user.username} created successfully")
        else:
            raise requests.exceptions.RequestException(
                f"Failed to create user {user.username} \n{response.text}"
            )

    def get_user_token(self, username, password):
        payload = {"username": username, "password": password}
        response = self.session.post("/auth/token/login", json=payload)

        if response.status_code >= 200 and response.status_code < 300:
            print("User token generated successfully")
            return response.json()
        else:
            raise requests.exceptions.RequestException(
                f"Failed to generate user token: {response.text}"
            )

    def authtenicat_user(self, token):
        response = self.session.get("/auth/users/me/", json={"token": token})

        if response.status_code >= 200 and response.status_code < 300:
            print("User token verified successfully")
        else:
            raise requests.exceptions.RequestException(
                f"Failed to verify user token: {response.text}"
            )
