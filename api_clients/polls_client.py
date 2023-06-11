import os
import requests


class PollsClient:
    def __init__(self, auth_token: str):
        self.url_base = os.getenv("BASE_URL")
        self.api_version = os.getenv("API_VERSION")

        self.request = requests.Session()
        self.base_url = f"{self.url_base}{self.api_version}"
        self.request.headers.update({"Content-Type": "application/json"})
        self.request.headers.update({"Authorization": f"Token {auth_token}"})

    def get_todays_poll(self) -> requests.Response:
        print("Getting today's poll")
        return self.request.get(f"{self.base_url}/polls/today/")

    def vote_for_restaurant(self, restaurant_id) -> requests.Response:
        print(f"Voting for restaurant with id: {restaurant_id}")
        payload = {"restaurant_id": restaurant_id}
        return self.request.post(f"{self.base_url}/polls/vote/", json=payload)

    def get_polls_history(self, from_date, to_date) -> requests.Response:
        print(f"Getting polls history from: {from_date} to: {to_date}")
        return self.request.get(
            f"{self.base_url}/polls/history/", params={"from": from_date, "to": to_date}
        )

    def reset_polls_for_date(self, date) -> requests.Response:
        print(f"Resetting polls for date: {date}")
        payload = {"date": date}
        return self.request.post(f"{self.base_url}/polls/reset/", json=payload)
