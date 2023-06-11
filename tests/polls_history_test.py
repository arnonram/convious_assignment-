import pytest
from api_clients.polls_client import PollsClient
from api_clients.restaurants_client import RestaurantsClient
from utils.date_utils import past_date, today
from utils.restaurants_utils import create_random_restaurants
from utils.users_utils import create_random_user

auth_token = create_random_user(1)[0].auth_token
pollsClient = PollsClient(auth_token)
restaurantClient = RestaurantsClient(auth_token)


@pytest.mark.usefixtures("cleanup_fixture")
class TestPollsHistory:
    def test_poll_history_for_past_week(self):
        restaurant_list = create_random_restaurants(restaurantClient, 5)
        for restaurant in restaurant_list:
            pollsClient.vote_for_restaurant(restaurant["id"])

        history_resp = pollsClient.get_polls_history(past_date(8), today())
        assert history_resp.status_code == 200

        history = history_resp.json()
        assert len(history) == 1
        for day in history:
            assert day["date"] is not None
            assert day["restaurant"] is not None
            assert isinstance(day["restaurant"]["id"], int)
            assert isinstance(day["restaurant"]["name"], str)

    def test_poll_history_for_past_week_not_including_today(self):
        restaurant_list = create_random_restaurants(restaurantClient, 5)
        for restaurant in restaurant_list:
            pollsClient.vote_for_restaurant(restaurant["id"])

        history_resp = pollsClient.get_polls_history(past_date(8), past_date(1))
        assert history_resp.status_code == 200

        history = history_resp.json()
        assert len(history) == 0
        for day in history:
            assert day["date"] is not None
            assert day["restaurant"] is not None
            assert isinstance(day["restaurant"]["id"], int)
            assert isinstance(day["restaurant"]["name"], str)

    def test_should_get_400_when_poll_history_with_malformed_dates(self):
        history_resp = pollsClient.get_polls_history("12-12-2023", today())
        assert history_resp.status_code == 400
        assert history_resp.json()["error"] == "Invalid from or to dates"

        history_resp = pollsClient.get_polls_history(today(), "12-2023-23")
        assert history_resp.status_code == 400
        assert history_resp.json()["error"] == "Invalid from or to dates"

    def test_should_get_400_when_poll_history_with_to_from_dates_are_reveres(self):
        history_resp = pollsClient.get_polls_history(today(), past_date(2))
        assert history_resp.status_code == 400
        assert history_resp.json()["error"] == "Invalid from or to dates"
