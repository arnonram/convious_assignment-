from faker import Faker
from api_clients.restaurants_client import RestaurantsClient


def create_random_restaurants(
    restaurants_client: RestaurantsClient, number_of_restaurants: int
):
    fake = Faker()
    restaurants = []
    for i in range(number_of_restaurants):
        restaurant_name = f"{fake.first_name()}'s Restaurant"
        resp = restaurants_client.create_restaurant(restaurant_name)
        restaurants.append({"name": restaurant_name, "id": resp["id"]})
    return restaurants


def delete_all_restaurants(restaurants_client: RestaurantsClient, restaurants):
    restaurants_client = RestaurantsClient()
    for restaurant in restaurants:
        restaurants_client.delete_restaurant(restaurant["id"])
