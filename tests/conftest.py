import pytest
from dotenv import load_dotenv
from faker import Faker

load_dotenv()


@pytest.fixture
def _faker():
    fake = Faker()
    return fake
