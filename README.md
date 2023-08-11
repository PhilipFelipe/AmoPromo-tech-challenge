# AmoPromo Flights Service
## Introduction
 The AmoPromo Flights service is responsible to process flight data from various airlines integrated APIs. With standardized data received from the APIs, it will create flights combinations based on the inputed parameters like the origin, destination, departure date, return date and the business rules.

 Besides that, this service also is responsible for maintaining our airports database fresh and updated!

 And finally, the service have authentication and is protected with tokens.

## Setup
 So, should we get it started and run our project?

 ### Lets start by cloning the repository!
 ```
 # SSH
 git clone git@github.com:PhilipFelipe/AmoPromo-tech-challenge.git
 # HTTP
 git clone https://github.com/PhilipFelipe/AmoPromo-tech-challenge.git
 ``` 

 ### Now, after cloning, it's necessary to configure the .env file!
 ```
SECRET_KEY = "YOUR-SECRET-KEY-HERE"
API_KEY = "YOUR-API-KEY-HERE"
USERNAME = "YOUR-USERNAME-HERE"
PASSWORD = "YOUR-PASSWORD-HERE"
 ```
 **Don't forget to rename the file from ".env-example" to ".env", ok?**

### Now, lets apply the Django migrations to setup our database
```
# Maybe just "py" will not work for you, so just try using "python3" instead
py manage.py makemigrations
py manage.py migrate
```

### Ok, now that our django and dabatase setup is done, what about we try running the docker?
```
docker-compose up --build

# or
docker compose up --build
```

### Nice, now our flights service is running! Let me explain how to use our API now
 So, first things first! For us to get going, it will be needed to create an user, right? So we'll be able to use our token and access the resources.
 ```
 # Endpoint for creating an user
 POST - http://localhost:8080/user/register
body: {
    "username": "jonh_doe",
    "password": "test123
}
response: {
    "token": "token-here"
}
 ```
### Cool, now we have the token! Let's try using it
```
# Our headers need to have an Authorization key
headers: {
    "Authorization": "Token {token}"
}
```

### Consulting our aiports
So, for consulting the airports, it'll be necessary to run a custom manage.py command, that will fill the database for the first time. Let's do it!
```
py manage.py import_airports
# or
python3 manage.py import_airports
```

Ok, now we are ready to go! 

Don't forget that we need our token to access this resource.
```
# The endpoint for consulting the airports
GET - http://localhost:8080/airport/list
```
 **Important**: When you send the first request, the data will be cached for one minute, during this time all requests will be obtained from the cache, with the exception of the airport database being updated with the custom command, in this case the cache will be reseted.


### Now, lets try searching for flights, tha main part isn't it?
So, for the flights we will need to send some parameters directly on the endpoint, let me show you
```
# Endpoint
GET - http://localhost:8080/flight/consult/:ORIGIN:/:DESTINATION:/:DEPARTURE_DATE:/:RETURN_DATE:
```
 Notice that we have some parameters to fill. Let me explain them:

 - ORIGIN: It's the airport that you want to depart from (GRU for example)
 - DESTINATION: It's the airport that you want to arrive to (STM for example)
 - DEPARTURE_DATE: It's the date (YYYY-MM-DD) that you want to depart
 - RETURN_DATE: It's the date (YYYY-MM-DD) that you want to return

### Ok but, what does this endpoint return?
Good question indeed, let me give you an example of its response
```
{
    "price": 3373.15,
    "outbound_flight": {
      "departure_date": "2023-08-11",
      "currency": "BRL",
      "origin": {
        "iata": "GRU",
        "city": "São Paulo",
        "latitude": -23.425669,
        "longitude": -46.481926,
        "state": "SP"
      },
      "destination": {
        "iata": "STM",
        "city": "Santarem",
        "latitude": -2.424886,
        "longitude": -54.78639,
        "state": "PA"
      },
      "departure_time": "2023-08-11T16:15:00",
      "arrival_time": "2023-08-11T19:15:00",
      "price": {
        "fare": 1370.67,
        "fees": 137.07,
        "total": 1507.74
      },
      "aircraft": {
        "model": "A 320",
        "manufacturer": "Airbus"
      },
      "meta": {
        "range": 2500.5,
        "cruise_speed_kmh": 833.5,
        "cost_per_km": 0.55
      }
    },
    "return_flight": {
      "departure_date": "2023-08-15",
      "currency": "BRL",
      "origin": {
        "iata": "STM",
        "city": "Santarem",
        "latitude": -2.424886,
        "longitude": -54.78639,
        "state": "PA"
      },
      "destination": {
        "iata": "GRU",
        "city": "São Paulo",
        "latitude": -23.425669,
        "longitude": -46.481926,
        "state": "SP"
      },
      "departure_time": "2023-08-15T05:45:00",
      "arrival_time": "2023-08-15T08:45:00",
      "price": {
        "fare": 1695.83,
        "fees": 169.58,
        "total": 1865.41
      },
      "aircraft": {
        "model": "A 320",
        "manufacturer": "Airbus"
      },
      "meta": {
        "range": 2500.5,
        "cruise_speed_kmh": 833.5,
        "cost_per_km": 0.68
      }
    }
  }
```
Basically it returns a list of flights combinations, with outbound flights and return flights, with the final price and all the information about both flights!

### Now, the last thing, the tests!
 There are some tests on our service and you can run them with the command below
 ```
 pytest
 ```

 That's it! Now you are free to try and search differente flights combinations and get the best prices!

 **Notes: There are validations on the parameters of the flights request, which where requested and also the combinations are ordered by the price (cheaper to expensive)**

 ## About the technologies
This project was made with the **Python v3.10**, which is a powerful and flexible language!
  
To work along and turn this process much easier, the **Django Framework** was used! It's a complete and robust web framework that allows us to work both the front-end and back-end, but in this case it was used only for the back-end with the **django-rest-framework**.

For the **database**, due to it's simplicity, the **sqlite3** was used. It is fast, simple and performatic for our purpose here!

To the **authentication**, it was used the own django-rest-framework auth token

**Sensitive data** should be secured and not exposed! For that it was used the **python-dotenv** lib, which allows us to load the .env file and use it on our application.

Finally, for the **tests**, it was used the **pytest** lib, which is also simple, performatic and well-known!

## Personal commentary
 I know this topic was not required, but, I just want to mention that I really enjoyed this challenge! It was so good to think and feel free to solve a problem with my own concepts and ideas! Its far away from good haha, but It was made with love and dedication (and some vague hours haha). I'm just grateful for that, thank you guys from AmoPromo :)