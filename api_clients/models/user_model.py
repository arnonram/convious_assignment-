from dataclasses import dataclass


@dataclass
class User:
    username: str
    email: str
    password: str


class UsersTokens:
    def __init__(self, username: str, auth_token: str):
        self.username = username
        self.auth_token = auth_token
