import connectDB
from config import *

table = connectDB.SQL_CRUD(user=user,
                           password=password,
                           host=host,
                           port=port,
                           dbname=database,
                           table=table)

# my_query = "INSERT INTO users values (1, 'admin', 'password', 'admin@gmail.com')"

table.connect()

table.insert(
    user_id=1,
    username='admin',
    password='password',
    email='kumarsurya.developer@gmail.com'
)

table.commit()

table.select_all()

'''
[IF NOT EXISTS] 
CREATE TABLE users (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL,
);

CREATE TABLE alerts (
	alert_id serial PRIMARY KEY,
	user_id NOT NULL,
	crypto_code VARCHAR ( 50 ) NOT NULL,
	trigger_value NUMERIC NOT NULL,
	status VARCHAR ( 255 ) UNIQUE NOT NULL,
);
'''