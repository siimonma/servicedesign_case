# Service Design - Coffee Review API
Welcome to ***Ali Chehades*** and ***Simon Martinssons*** case assignment for Service Design course, IoT class -22 at KYH.
This is an API designed for reviewing swedish coffee products.

The API server is based on _Flask_ and is run on _localhost:5000_ as a default. To start the API server, run the project from 
**main.py**. 

### First time use
To initiate both databases and start the webscraper, run the project with the _initiate_ parameter set to _True_ for the coffeeInfoJSON instance (Set to True as default).
This will create two database files, **coffee.db** and **data.json**, located under directory 'databases'. 
The data.json-file will contain all the coffee products while the coffee.db will have the empty tables _Users_, _Users_auth_ and _Reviews_.

### Restarting server
If you need to restart the server and do not want to web scrape again, set the _initiate_ parameter to _False_ for the coffeeInfoJSON instance before you run the project again.

## Documentation
