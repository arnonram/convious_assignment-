import pytest
from api_clients.polls_client import PollsClient
from api_clients.restaurants_client import RestaurantsClient
from utils.date_utils import today
from utils.restaurants_utils import (
    create_random_restaurants,
    extract_resturant_data_from_rankings,
)
from utils.users_utils import create_random_user


auth_token = create_random_user(1)[0].auth_token
restaurantClient = RestaurantsClient(auth_token)
pollsClient = PollsClient(auth_token)


@pytest.mark.usefixtures("cleanup_fixture")
class TestPollsVotes:
    def test_should_recieive_error_when_voting_more_than_5_times_same_date(self):
        pollsClient.reset_polls_for_date(today())
        restaurant_list = create_random_restaurants(restaurantClient, 5)

        for index, restaurant in enumerate(restaurant_list):
            vote_resp = pollsClient.vote_for_restaurant(restaurant["id"])
            assert vote_resp.status_code == 201
            assert vote_resp.json()["available_votes"] == 5 - (index + 1)

        vote_resp = pollsClient.vote_for_restaurant(restaurant_list[0]["id"])
        assert vote_resp.status_code == 400
        assert vote_resp.json()["error"] == "Votes per day exceeded"

    def test_restaurant_should_have_score_of_9_when_same_user_votes_all_daily_votes_for_one_restaurant(
        self,
        _faker,
    ):
        pollsClient.reset_polls_for_date(today())
        create_resp = restaurantClient.create_restaurant(
            f"{_faker.first_name()} Restaurant"
        )
        assert create_resp.status_code == 201
        user = create_random_user(1)

        expected_vote_score = [4, 6, 7, 8, 9]
        for expected in expected_vote_score:
            user_under_test_client = PollsClient(user[0].auth_token)
            vote_resp = user_under_test_client.vote_for_restaurant(
                create_resp.json()["id"]
            )
            assert vote_resp.status_code == 201
            restaurant_data = extract_resturant_data_from_rankings(
                vote_resp.json()["rankings"], create_resp.json()["id"]
            )
            assert restaurant_data["score"] == expected
            assert restaurant_data["voters"] == 1

    def test_different_restaurants_should_have_score_of_4_when_same_user_votes_for_them_first_time(
        self,
    ):
        pollsClient.reset_polls_for_date(today())
        restaurant_list = create_random_restaurants(restaurantClient, 5)
        user = create_random_user(1)

        for restaurant in restaurant_list:
            user_under_test_client = PollsClient(user[0].auth_token)
            vote_resp = user_under_test_client.vote_for_restaurant(restaurant["id"])
            assert vote_resp.status_code == 201
            restaurant_data = extract_resturant_data_from_rankings(
                vote_resp.json()["rankings"], restaurant["id"]
            )
            assert restaurant_data["score"] == 4

    def test_restaurant_score_should_multiply_by_4_for_each_unique_voter(self):
        pollsClient.reset_polls_for_date(today())
        create_resp = create_random_restaurants(restaurantClient, 1)[0]

        users = create_random_user(3)
        for index, user in enumerate(users):
            user_under_test_client = PollsClient(user.auth_token)
            vote_resp = user_under_test_client.vote_for_restaurant(create_resp["id"])
            assert vote_resp.status_code == 201
            restaurant_data = extract_resturant_data_from_rankings(
                vote_resp.json()["rankings"], create_resp["id"]
            )

            assert restaurant_data["voters"] == index + 1
            assert restaurant_data["score"] == (index + 1) * 4

    def test_restaurant_should_be_top_when_same_score_as_other_but_different_voters_number(
        self,
    ):
        pollsClient.reset_polls_for_date(today())
        restauran_list = create_random_restaurants(restaurantClient, 2)
        users = create_random_user(3)

        user_one = PollsClient(users[0].auth_token)
        user_two = PollsClient(users[1].auth_token)
        user_three = PollsClient(users[2].auth_token)

        user_one.vote_for_restaurant(restauran_list[0]["id"])
        user_two.vote_for_restaurant(restauran_list[0]["id"])

        for i in range(4):
            user_three.vote_for_restaurant(restauran_list[1]["id"])

        todays_poll = pollsClient.get_todays_poll()
        assert todays_poll.status_code == 200
        assert todays_poll.json()["top"]["id"] == restauran_list[0]["id"]
        assert todays_poll.json()["top"]["score"] == 8
        assert todays_poll.json()["top"]["voters"] == 2

    def test_should_get_400_when_voting_for_non_existent_restaurant(self):
        pollsClient.reset_polls_for_date(today())
        vote_resp = pollsClient.vote_for_restaurant(999999)
        assert vote_resp.status_code == 400
        assert vote_resp.json()["error"] == "Restaurant does not exist"

    def test_should_get_400_when_voting_with_None_as_restaurant_name(self):
        pollsClient.reset_polls_for_date(today())
        vote_resp = pollsClient.vote_for_restaurant(None)
        assert vote_resp.status_code == 400
        assert vote_resp.json()["error"] == "Restaurant does not exist"

    def test_should_get_OK_when_reset_poll_and_votes_are_reset(self):
        restauran_list = create_random_restaurants(restaurantClient, 2)
        users = create_random_user(2)

        self.vote_all_users_restaurants_and_verify(restauran_list, users)

        reset_resp = pollsClient.reset_polls_for_date(today())
        assert reset_resp.status_code == 200
        assert reset_resp.json() == {"ok": True}

        todays_poll = pollsClient.get_todays_poll()
        rankings = todays_poll.json()["rankings"]
        assert todays_poll.json()["top"]["score"] == 0
        for restaurant in rankings:
            assert restaurant["score"] == 0
            assert restaurant["voters"] == 0

        self.vote_all_users_restaurants_and_verify(restauran_list, users)

    def test_should_get_OK_when_reset_poll_for_non_existent_date(self):
        reset_resp = pollsClient.reset_polls_for_date("3001-12-12")
        assert reset_resp.status_code == 200
        assert reset_resp.json() == {"ok": True}

    def test_should_get_400_when_reset_poll_for_malformed_date(self):
        reset_resp = pollsClient.reset_polls_for_date("12-3001-12")
        assert reset_resp.status_code == 400
        reset_resp = pollsClient.reset_polls_for_date("12-12-3001")
        assert reset_resp.status_code == 400

    # Test Utils functions
    def vote_all_users_restaurants_and_verify(self, restauran_list, users):
        for user in users:
            for restaurant in restauran_list:
                user_under_test_client = PollsClient(user.auth_token)
                user_under_test_client.vote_for_restaurant(restaurant["id"])

        todays_poll = pollsClient.get_todays_poll()
        assert todays_poll.json()["top"]["score"] > 4
