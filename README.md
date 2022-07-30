# krypto-backend-alerttool

Creating a price alert application that triggers an email when the user’s target price is
achieved. 
By :- V Surya Kumar (19BCE10286)


## INSTALLATION
Pull the repository and Check out all the files in your local directory.

Follow the below steps to make it run:

### 1. Setting up database


### 2. Setting up RabbitMQ (using docker)


### 3. Getting API key for Binance Websockets


### 4. Running the CodeBase


## USING THE API

### 1. Signing Up
Endpoint: 

    "/signup"

Parameters:

    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


### 2. Logging In
Endpoint: 

    "/login"

Parameters:

    email: str = Field(..., description="user email")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


### 3. CREAT ALERT API
Endpoint: 

    "/alert/create"

Parameters:

    crypto_code: str
    trigger_price: float


### 4. Fetch Alerts API
Endpoint: 

    "/alert"

Parameters:

    status: str = ""
    (optional filter: CREATED, TRIGGERED, DELETED)

### 5. Update Alerts API
Endpoint: 

    "/alert/delete"

Parameters:

    alert_id: int
    (TO Update)
    


Refer to the following doc for detailed information:
https://docs.google.com/document/d/1sDexMTX7-0CSUQk_iu9KzK70T5yowgZht6xtzl3B_mU/edit?usp=sharing


