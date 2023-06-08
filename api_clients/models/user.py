class User:
    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password


class UsersTokens:
    def __init__(self, username: str, auth_token: str):
        self.username = username
        self.auth_token = auth_token
