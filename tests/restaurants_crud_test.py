from api_clients.restaurants_client import RestaurantsClient
from api_clients.users_client import UsersClient
from utils.restaurants_utils import create_random_restaurants


user_client = UsersClient()
auth_token = user_client.get_user_token()
restaurantClient = RestaurantsClient(auth_token)


def test_create_restaurant(_faker):
    name = _faker.first_name()
    create_resp = restaurantClient.create_restaurant(f"{name}'s Restaurant")
    assert create_resp.status_code == 201
    print(create_resp.json()["id"])
    assert create_resp.json()["name"] == f"{name}'s Restaurant"
    assert isinstance(create_resp.json()["id"], int)


def test_create_restaurant_with_empty_name():
    create_resp = restaurantClient.create_restaurant("")
    assert create_resp.status_code == 400
    assert create_resp.json()["name"][0] == "This field may not be blank."


def test_create_restaurant_with_duplicate_name(_faker):
    name = _faker.first_name()
    create_resp = restaurantClient.create_restaurant(f"{name}'s Restaurant")
    assert create_resp.status_code == 201
    print(create_resp.json()["id"])
    assert create_resp.json()["name"] == f"{name}'s Restaurant"
    assert isinstance(create_resp.json()["id"], int)

    create_resp = restaurantClient.create_restaurant(f"{name}'s Restaurant")
    assert create_resp.status_code == 400
    assert create_resp.json()["name"][0] == "restaurant with this name already exists."


def test_get_all_restaurants():
    create_random_restaurants(restaurantClient, 3)
    get_all_resp = restaurantClient.get_restaurants()
    assert get_all_resp.status_code == 200
    print(len(get_all_resp.json()))
    assert len(get_all_resp.json()) >= 3


def test_update_restaurant(_faker):
    create_resp = restaurantClient.create_restaurant(
        f"{_faker.first_name()} Restaurant"
    )
    assert create_resp.status_code == 201

    update_resp = restaurantClient.update_restaurant(
        create_resp.json()["id"], "Updated Restaurant"
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Updated Restaurant"


def test_update_restaurant_with_empty_name(_faker):
    create_resp = restaurantClient.create_restaurant(
        f"{_faker.first_name()} Restaurant"
    )
    assert create_resp.status_code == 201

    update_resp = restaurantClient.update_restaurant(create_resp.json()["id"], "")
    assert update_resp.status_code == 400
    assert update_resp.json()["name"][0] == "This field may not be blank."


def test_update_non_existent_restaurant():
    update_resp = restaurantClient.update_restaurant(9999999999, "Updated Restaurant")
    assert update_resp.status_code == 404
    assert update_resp.json()["detail"] == "Not found."


def test_delete_restaurant(_faker):
    create_resp = restaurantClient.create_restaurant(
        f"{_faker.first_name()} Restaurant"
    )
    assert create_resp.status_code == 201

    del_resp = restaurantClient.delete_restaurant(create_resp.json()["id"])
    assert del_resp.status_code == 204


def test_delete_non_existent_restaurant():
    del_resp = restaurantClient.delete_restaurant(9999999999)
    assert del_resp.status_code == 404
    assert del_resp.json()["detail"] == "Not found."
