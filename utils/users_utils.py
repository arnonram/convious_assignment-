from typing import List
from faker import Faker
from api_clients.models.user_model import User, UsersTokens
from api_clients.users_client import UsersClient


def create_random_user(number_of_users: int) -> List:
    users_tokens = []
    user_client = UsersClient()
    users = create_users_list(number_of_users)
    for user in users:
        user_client.create_user(user)
    for user in users:
        resp_token = user_client.get_user_token(user.username, user.password)
        users_tokens.append(UsersTokens(user.username, resp_token))
    return users_tokens


def create_users_list(number_of_users: int) -> List:
    fake = Faker()
    users = []
    for i in range(number_of_users):
        user_name = fake.user_name()
        user = User(
            f"{fake.user_name()}_{i}",
            f"{user_name}@{fake.free_email_domain()}",
            fake.password(length=10),
        )
        users.append(user)
    return users
