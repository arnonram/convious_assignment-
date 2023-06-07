import requests
from api_clients.bae_client_session import BaseClientSession


class PollsClient:
    def __init__(self):
        self.session = BaseClientSession()

    def get_todays_poll(self):
        response = self.session.get("/polls/today/")
        if response.status_code >= 200 and response.status_code < 300:
            print("Polls list retrieved successfully")
            return response.json()
        else:
            raise requests.exceptions.RequestException(
                f"Failed to retrieve polls list: \n{response.text}"
            )

    def vote_for_restaurant(self, restaurant_id):
        payload = {"restaurant_id": restaurant_id}
        response = self.session.post("/polls/vote/", json=payload)
        if response.status_code >= 200 and response.status_code < 300:
            print(f"Added vote to {restaurant_id}")
            return response.json()
        else:
            raise requests.exceptions.RequestException(
                f"Failed to vote for restaurant {restaurant_id} \n{response.text}"
            )

    def get_polls_history(self, from_date, to_date):
        response = self.session.get(
            "/polls/history/", params={"from": from_date, "to": to_date}
        )
        if response.status_code >= 200 and response.status_code < 300:
            print("Polls history retrieved successfully")
            return response.json()
        else:
            raise requests.exceptions.RequestException(
                f"Failed to retrieve polls history: \n{response.text}"
            )

    def reset_polls_for_date(self, date):
        payload = {"date": date}
        response = self.session.post("/polls/reset/", json=payload)
        if response.status_code >= 200 and response.status_code < 300:
            print("Polls reset successfully")
            return response.json()
        else:
            raise requests.exceptions.RequestException(
                f"Failed to reset polls: \n{response.text}"
            )
