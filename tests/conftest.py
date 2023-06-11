import pytest
from dotenv import load_dotenv
from faker import Faker
from api_clients.restaurants_client import RestaurantsClient
from utils.restaurants_utils import delete_all_restaurants
from utils.users_utils import create_random_user

load_dotenv()


@pytest.fixture(scope="module")
def cleanup_fixture():
    yield
    auth_token = create_random_user(1)[0].auth_token
    restaurantClient = RestaurantsClient(auth_token)
    print("Deleting all restaurants")
    delete_all_restaurants(restaurantClient)


@pytest.fixture
def _faker():
    fake = Faker()
    return fake
