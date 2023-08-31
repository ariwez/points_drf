# Points DRF API

1. create `.env` file based on `.env.dist`
2. `make run-app` to start the app at http://localhost:8000
3. `make run-migrate` to apply migrations
4. `make run-import-users-data` to import users from `users.csv` file (or use `python manage.py import_users_data <path_to_file>`
    in docker container)
5. `make run-tests` to run tests

- List of users with their points balance: http://localhost:8000/api/points/
- Subpage with form to add/remove points is available from list view.
- Swagger documentation is available at http://localhost:8000/swagger

### Assumptions:
- first name, last name, email are required fields,
- user's email is unique and is used to identify user,
- if `users.csv` contains invalid data (e.g. invalid balance) it will be skipped and logged,
- if `users.csv` contains invalid referral user (e.g. user does not exist in system) it will be skipped and logged,
- ids (row numbers) from `users.csv` are not imported (database ids are used)
- points balance can be negative as described in the task, no maximum/minimum value is set,
- points sources are kept in separate table to allow adding new sources in the future (via admin panel), initial sources are created
  during migration,
- changing balance requires existing points source,
- points history keeps points changes made with service after account creation 
- permissions are not implemented (all endpoints are public),

### Possible improvements:
- when balance is changed receiver is using account's `post_save` signal when handler will raise exception it will rollback
  transaction - should be clarified with product owner if this is the desired behaviour, sending emails could be moved
  to queue and executed asynchronously,
- add points maximum/minimum value and validate it during points addition/subtraction,
- separate sources by deposit/withdrawal and validate if user has enough points to withdraw,
- using custom user model based on Django more suited to the project scope (authentication, registration,
  account management),
- using context manager for signal disconnect/connect,
- add csv schema validation,
- adding context to source (e.g. referred user id, tournament id etc.)
- worth consideration is disconnecting balance change signals in tests environment,
- testing receivers should mock method called inside handler (e.g. send_email),

### Known issues:
- users.csv contains row with invalid balance ('59O' - should be '590'),
- users.csv contains row with invalid referral user ('oscarsbrookiq@wikispaces.com' does not exist in system),
- api is using html templates so requests from swagger are not accepted (fixable by using json renderer),
