from api_clients.polls_client import PollsClient
from api_clients.restaurants_client import RestaurantsClient


restaurantClient = RestaurantsClient("dummy_auth_token")
pollsClient = PollsClient("dummy_auth_token")


class TestForUnauthorizedUsers:
    def test_should_get_401_when_auth_token_is_invalid_for_restaurants_apis(self):
        create_restaurant = restaurantClient.create_restaurant("dummy_name")
        self.assert_invalid_token_errors(create_restaurant)

        get_restaurants = restaurantClient.get_restaurants()
        self.assert_invalid_token_errors(get_restaurants)

        update_restaurant = restaurantClient.update_restaurant(1, "dummy_name")
        self.assert_invalid_token_errors(update_restaurant)

        delete_restaurant = restaurantClient.delete_restaurant(1)
        self.assert_invalid_token_errors(delete_restaurant)

    def test_should_get_401_when_auth_token_is_invalid_for_polls_apis(self):
        get_polls_for_date = pollsClient.get_todays_poll()
        self.assert_invalid_token_errors(get_polls_for_date)

        vote_for_restaurant = pollsClient.vote_for_restaurant(1)
        self.assert_invalid_token_errors(vote_for_restaurant)

        reset_polls = pollsClient.reset_polls_for_date("dummy_date")
        self.assert_invalid_token_errors(reset_polls)

        get_polls_history = pollsClient.get_polls_history(
            "dummy_from_date", "dummy_to_date"
        )
        self.assert_invalid_token_errors(get_polls_history)

    def assert_invalid_token_errors(self, response):
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid token."
