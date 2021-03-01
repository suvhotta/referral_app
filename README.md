# referral_app
Referral system built using Django rest framework.

## Local Setup
```
$ git clone https://github.com/suvhotta/referral_app.git
$ cd referral_project
$ pipenv install
$ pipenv shell
$ python manage.py makemigrations
$ python manage.py migrate
```
If you're having issues with the db migrations, please ensure you've postgres installed on your machine and it has a referral database. You can check the settings.py file for further info.
Also you need to create an API_Key from Sendgrid in order to access the mail sending feature.
## Run
```
$ python manage.py runserver
```
## Structure

In a RESTful API, endpoints (URLs) define the structure of the API and how end users access data from our application using various HTTP methods.
| Endpoint    | HTTP Method |  CRUD | RESULT                |
| ----------- | ----------- | ------|--------               |
| register    | POST        | CREATE | creates new user     |
| login       | GET         | CREATE   | creates token for user authentication   |
| wallet  | GET         | READ   | To get wallet details for user     |
| referral  | GET      | READ | To check user's referral code   |
| referral  | POST      | READ | To send referral code   |
