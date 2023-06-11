import string
import pytest
from api_clients.restaurants_client import RestaurantsClient
from utils.restaurants_utils import create_random_restaurants
from utils.users_utils import create_random_user


auth_token = create_random_user(1)[0].auth_token
restaurantClient = RestaurantsClient(auth_token)


@pytest.mark.usefixtures("cleanup_fixture")
class TestRestaurantsCRUD:
    def test_should_get_201_when_create_restaurant(self, _faker):
        name = _faker.first_name()
        create_resp = restaurantClient.create_restaurant(f"{name}'s Restaurant")
        assert create_resp.status_code == 201
        print(create_resp.json()["id"])
        assert create_resp.json()["name"] == f"{name}'s Restaurant"
        assert isinstance(create_resp.json()["id"], int)

    def test_should_create_restaurant_with_special_characters(self):
        special_chars = string.punctuation
        for char in special_chars:
            create_resp = restaurantClient.create_restaurant(
                f"Restaurant {char} Is Open"
            )
            assert create_resp.status_code == 201
            assert create_resp.json()["name"] == f"Restaurant {char} Is Open"

    def test_should_create_restaurant_with_random_alphanumeric_and_special_chars(
        self, _faker
    ):
        for i in range(30):
            name = _faker.password(length=25, special_chars=True, digits=True)
            create_resp = restaurantClient.create_restaurant(name)
            assert create_resp.status_code == 201
            assert create_resp.json()["name"] == name

    @pytest.mark.parametrize("char_length", [50, 100, 200, 201])
    def test_should_shorten_restaurant_with_255_characters(self, _faker, char_length):
        name = _faker.text(max_nb_chars=char_length)
        create_resp = restaurantClient.create_restaurant(name)
        if char_length <= 200:
            assert create_resp.status_code == 201
            assert create_resp.json()["name"] == name
        else:
            assert create_resp.status_code == 400
            assert (
                create_resp.json()["details"]
                == "Ensure this field has no more than 200 characters."
            )

    def test_should_get_400_when_create_restaurant_with_empty_name(
        self,
    ):
        create_resp = restaurantClient.create_restaurant("")
        assert create_resp.status_code == 400
        assert create_resp.json()["name"][0] == "This field may not be blank."

    def test_should_get_400_when_with_name_None(
        self,
    ):
        create_resp = restaurantClient.create_restaurant(None)
        assert create_resp.status_code == 400
        assert create_resp.json()["name"][0] == "This field may not be null."

    def test_should_get_400_when_create_restaurant_with_duplicate_name(self, _faker):
        name = _faker.first_name()
        create_resp = restaurantClient.create_restaurant(f"{name}'s Restaurant")
        assert create_resp.status_code == 201
        print(create_resp.json()["id"])
        assert create_resp.json()["name"] == f"{name}'s Restaurant"
        assert isinstance(create_resp.json()["id"], int)

        create_resp = restaurantClient.create_restaurant(f"{name}'s Restaurant")
        assert create_resp.status_code == 400
        assert (
            create_resp.json()["name"][0] == "Restaurant with this name already exists."
        )

    def test_should_get_list_of_all_restaurants_when_calling_get_all_restaurants_api(
        self,
    ):
        create_random_restaurants(restaurantClient, 3)
        get_all_resp = restaurantClient.get_restaurants()
        assert get_all_resp.status_code == 200
        print(len(get_all_resp.json()))
        assert len(get_all_resp.json()) >= 3

    def test_should_get_200_and_updated_name_when_updating_restaurant_name(
        self, _faker
    ):
        create_resp = restaurantClient.create_restaurant(
            f"{_faker.first_name()} Restaurant"
        )
        assert create_resp.status_code == 201

        update_resp = restaurantClient.update_restaurant(
            create_resp.json()["id"], "Updated Restaurant"
        )
        assert update_resp.status_code == 200
        assert update_resp.json()["name"] == "Updated Restaurant"

    def test_should_get_404_when_update_restaurant_with_empty_name(self, _faker):
        create_resp = restaurantClient.create_restaurant(
            f"{_faker.first_name()} Restaurant"
        )
        assert create_resp.status_code == 201

        update_resp = restaurantClient.update_restaurant(create_resp.json()["id"], "")
        assert update_resp.status_code == 400
        assert update_resp.json()["name"][0] == "This field may not be blank."

    def test_should_get_404_when_update_non_existent_restaurant(
        self,
    ):
        update_resp = restaurantClient.update_restaurant(
            9999999999, "Updated Restaurant"
        )
        assert update_resp.status_code == 404
        assert update_resp.json()["detail"] == "Not found."

    def test_should_get_201_when_delete_restaurant_and_delete_only_selected_restaurant(
        self,
    ):
        create_resp = create_random_restaurants(restaurantClient, 5)
        get_restaurant_resp = restaurantClient.get_restaurants()
        total_restaurants = len(get_restaurant_resp.json())

        del_resp = restaurantClient.delete_restaurant(create_resp[0]["id"])
        assert del_resp.status_code == 204

        get_restaurant_resp = restaurantClient.get_restaurants()
        for restaurant in get_restaurant_resp.json():
            assert restaurant["id"] != create_resp[0]["id"]
        assert len(get_restaurant_resp.json()) == total_restaurants - 1

    def test_should_get_404_when_delete_non_existent_restaurant(self):
        del_resp = restaurantClient.delete_restaurant(9999999999)
        assert del_resp.status_code == 404
        assert del_resp.json()["detail"] == "Not found."
