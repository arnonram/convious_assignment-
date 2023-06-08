# Convious Assignment

## High level test plan

1. CRUD tests for all **Restaurants APIs**
   - Starting with "happy flow" tests
   - Then leading to negative tests, such as:
     - Create restaurant API without `name` / incorrect payload properties
     - Create restaurant API with already existing restaurant (same and different name case, for example: 'My Res' and 'my RES' are the same)
     - Delete/Update non-existing restaurant
2. **Polls APIs**
   - Again, starting with "happy flow" tests
     - here we will also verify that scoring is correct
   - Negative tests:
     - voting over limit
     - voting for non-exxisting restaurant
     - votig for restaurant but sending non-number / votig for restaurant but incorrect payload
     - getting poll history when `to` is greated than `from`
     - reseting poll for future/non-existing date
3. Testing that when sending incorrect `auth_token` results in a forbidden response
