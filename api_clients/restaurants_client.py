import requests
from api_clients.bae_client_session import BaseClientSession


class RestaurantsClient:
    def __init__(self):
        self.session = BaseClientSession()

    def get_restaurants(self):
        response = self.session.get("/restaurants/")
        if response.status_code >= 200 and response.status_code < 300:
            print("Restaurants list retrieved successfully")
            return response.json()
        else:
            raise requests.exceptions.RequestException(
                f"Failed to retrieve restaurants list: \n{response.text}"
            )

    def create_restaurant(self, name):
        payload = {"name": name}
        response = self.session.post("/restaurants/", json=payload)
        if response.status_code >= 200 and response.status_code < 300:
            print("Restaurant created successfully")
            return response.json()
        else:
            raise requests.exceptions.RequestException(
                f"Failed to create restaurant: \n{response.text}"
            )

    def update_restaurant(self, id, name):
        payload = {"name": name}
        response = self.session.put(f"/restaurants/{id}/", json=payload)
        if response.status_code >= 200 and response.status_code < 300:
            print("Restaurant updated successfully")
            return response.json()
        else:
            raise requests.exceptions.RequestException(
                f"Failed to update restaurant: \n{response.text}"
            )

    def delete_restaurant(self, id):
        response = self.session.delete(f"/restaurants/{id}/")
        if response.status_code >= 200 and response.status_code < 300:
            print("Restaurant deleted successfully")
            return response.json()
        else:
            raise requests.exceptions.RequestException(
                f"Failed to delete restaurant: \n{response.text}"
            )
