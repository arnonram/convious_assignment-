import os
import pytest
from api_clients.restaurants_client import RestaurantsClient
from api_clients.users_client import UsersClient
from dotenv import load_dotenv
from faker import Faker

from utils.restaurants_utils import create_random_restaurants


@pytest.fixture(scope="session", autouse=True)
def setup(self):
    load_dotenv()
    self.fake = Faker()
    resp = UsersClient().get_user_token(
        os.getenv("BASE_USER"), os.getenv("BASE_PASSWORD")
    )
    self.client = RestaurantsClient(resp)


def create_restaurant_test(self):
    resp = self.client.create_restaurant(f"{self.fake.first_name()} Restaurant")
    assert resp.status_code == 200
    assert resp.json()["name"] == "Test Restaurant"


def get_all_restaurnats_test(self):
    create_random_restaurants(self.client, 10)
    resp = self.client.get_restaurants()
    assert resp.status_code == 200
    assert len(resp.json()) >= 10
