from datetime import date
from api_clients.polls_client import PollsClient
from api_clients.restaurants_client import RestaurantsClient
from api_clients.users_client import UsersClient
from utils.date_utils import format_date, past_date, today
from utils.restaurants_utils import create_random_restaurants


user_client = UsersClient()
auth_token = user_client.get_user_token()
restaurantClient = RestaurantsClient(auth_token)
pollsClient = PollsClient(auth_token)


def test_first_vote(_faker):
    create_resp = restaurantClient.create_restaurant(
        f"{_faker.first_name()} Restaurant"
    )
    assert create_resp.status_code == 201

    vote_resp = pollsClient.vote_for_restaurant(create_resp.json()["id"])
    assert vote_resp.status_code == 201

    assert vote_resp.json()["top"]["id"] == create_resp.json()["id"]
    assert vote_resp.json()["top"]["score"] == 4
    assert vote_resp.json()["top"]["voters"] == 1


def test_reset_polls():
    reset_resp = pollsClient.reset_polls_for_date(today())
    assert reset_resp.status_code == 200
    assert reset_resp.json() == {"ok": True}


def test_reset_polls_future_date():
    reset_resp = pollsClient.reset_polls_for_date("3001-12-12")
    assert reset_resp.status_code == 200
    assert reset_resp.json() == {"ok": True}


def test_poll_history():
    history_resp = pollsClient.get_polls_history(past_date(2), today())
    assert history_resp.status_code == 200
    assert len(history_resp.json()) >= 1
