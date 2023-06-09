# Convious Assignment

## High level test plan

1. CRUD tests for all **Restaurants APIs**
   - Starting with "happy flow" tests
   - Then leading to negative tests, such as:
     - Create restaurant API without `name`
     - Creating resaurants with special chars, etc..
     - Create restaurant API with already existing restaurant (same and different name case, for example: 'My Res' and 'my RES' are the same)
     - Delete/Update non-existing restaurant
1. **Polls APIs**
   - Again, starting with "happy flow" tests
     - here we will also verify that scoring is correct
   - Negative tests:
     - Voting over limit
     - Voting for non-exxisting restaurant
     - Votig for restaurant but sending non-number / voting for restaurant but incorrect payload
     - Getting poll history when `to` is greated than `from`
     - Malformed dates
     - Reseting poll for future/non-existing date
1. Testing that when sending incorrect `auth_token` results in a forbidden response
1. Writing performance tests for these APIs using Locust (for example) in order to test load, stress, etc.. of the APIs and system.
   - **_Note:_** Performance testing is out of scope for this assignment

## How to run

1. Create venv
1. Run:
   ```bash
   pip install -r requirements.txt
   ```
1. Verify you have a `PYTHONPATH` env var configured to project root
1. Run in terminal:
   ```bash
   pytest
   ```

## Bugs Found

1. Documentation issue: `GET /api/v1/polls/history/?from2019-06-10&to=2019-06-12` => should be `from=2019-06-10`
1. Can create restaurant with duplicate name
1. Creating restaurant with more than 200 characters give a `201` status (success) with a `{"name": "Ensure this field has no more than 200 characters"}`. This should probably be a 400 error, and name should be `detail` or `error`

## Comments

- Should notify when two restaurants have same `score` and same number of `voters`. At the moment it takes the one with the lowers `id`. This a product decision.
- Tests dealing with dates and scheduling cannot be tested on a clean env. (such as polls history, and verifyin that votes are reset every day). Some ways to test them:
  - Injecting mock data or manipulating data in the DB.
  - Another way to test them (if performing API tests), is to mock the DB, and **spy** on the DB manipulation functions to verify they are sending correct requests
- At one point the test `test_should_create_restaurant_with_random_alphanumeric_and_special_chars` was creating a 100 restaurants one after the other and failed on a `502 error`
- Ideally, part of the clean-up would be to delete created users
