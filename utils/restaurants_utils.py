from faker import Faker
from api_clients.restaurants_client import RestaurantsClient


def create_random_restaurants(
    restaurants_client: RestaurantsClient, number_of_restaurants: int
):
    fake = Faker()
    restaurants = []
    for i in range(number_of_restaurants):
        restaurant_name = f"{fake.first_name()}'s {fake.country()} Restaurant"
        resp = restaurants_client.create_restaurant(restaurant_name)
        restaurants.append({"name": restaurant_name, "id": resp.json()["id"]})
    return restaurants


def delete_all_restaurants(restaurants_client: RestaurantsClient):
    all_restaurants = restaurants_client.get_restaurants()
    for restaurant in all_restaurants.json():
        restaurants_client.delete_restaurant(restaurant["id"])


def extract_resturant_data_from_rankings(rankins_array, restauarant_id: int):
    for restaurant in rankins_array:
        if restaurant["id"] == restauarant_id:
            return restaurant
