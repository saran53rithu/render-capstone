# CAPSTONE PROJECT - RENDER HOSTED

## Restaurant Management System

The Restaurant Management System is a web application designed to manage and display restaurant and menu details. It provides endpoints for adding, updating, and deleting restaurants and menu items, as well as retrieving information about them. The system is built using Flask, a popular Python web framework, and uses SQLAlchemy for database interactions.

### Features:

Restaurant Management

List Restaurants: Retrieve a list of all restaurants with their details including name, address, phone number, and email.
Add Restaurant: Add a new restaurant to the database by providing the name, address, phone number, and email.
Update Restaurant: Update details of an existing restaurant, such as name, address, phone number, and email.
Delete Restaurant: Remove a restaurant from the database by specifying its ID.

Menu Management

List Menus: Retrieve a list of all menu items, including name, price, description, availability, and associated restaurant ID.
Add Menu Item: Add a new menu item by specifying the name, price, description, availability, and the restaurant ID it belongs to.

### To test the project locally

Fork this project - https://github.com/saran53rithu/render-capstone

Setup this project by runnning this command - pip install -r requirements.txt

Create database tables - python create-db-tables.py

Run the app - flask run --reload

Test the application after generating valid token with required permissions from auth0 and run - pytest test-app.py

There are two roles associated with this project
1. Restaurant owner 
        get:restaurants-detail
        get:menu-detail
        post:restaurants-detail
        post:menu-detail
        update:restaurants-detail
        delete:restaurants-detail
3. Restaurant worker
        get:restaurants-detail
        get:menu-detail
        post:menu-detail

Restaurant owner has all access whereas restaurant worker can only view restaurant details, menu details and add new menu

### Render details

This applications is hosted in render url - https://render-capstone.onrender.com/

### API Endpoints:

Restaurant Endpoints:

GET /restaurants: Lists all restaurants.
POST /add-restaurant: Adds a new restaurant.
PATCH /restaurants/<int:restaurant_id>: Updates details of an existing restaurant.
DELETE /restaurants/<int:restaurant_id>: Deletes a specific restaurant.

Menu Endpoints:

GET /menus: Lists all menu items.
POST /add-menu: Adds a new menu item.


1. GET /restaurants
Description: Fetches the list of all restaurants.
Request Arguments: None
Returns: A JSON array of restaurant objects, each with id, name, address, phone_number, and email.
Example:

```json
[
    {
        "address": "123 Pasta St",
        "email": "contact@italianbistro.com",
        "id": 1,
        "name": "Italian Bistro",
        "phone_number": "555-1234"
    },
    {
        "address": "456 Sushi Ave",
        "email": "info@sushihaven.com",
        "id": 2,
        "name": "Sushi Haven",
        "phone_number": "555-5678"
    }
]
```

2. GET /menu
Description: Fetches the list of all menu items.
Request Arguments: None
Returns: A JSON array of menu items, each with id, name, price, description, available, and restaurant_id.
Example:

```json
[
    {
        "available": true,
        "description": "Classic Italian pasta with cream and bacon",
        "id": 1,
        "name": "Spaghetti Carbonara",
        "price": "12.99",
        "restaurant_id": 1
    },
    {
        "available": true,
        "description": "Simple pizza with tomato, mozzarella, and basil",
        "id": 2,
        "name": "Margherita Pizza",
        "price": "9.99",
        "restaurant_id": 1
    }
]
```

3. POST /add-restaurant
Description: Adds a new restaurant to the database.
Request Arguments: JSON object with name, address, phone_number, and email.
Example:

```json
{
    "name": "New Restaurant",
    "address": "789 New Place",
    "phone_number": "555-0000",
    "email": "contact@newrestaurant.com"
}
```
Success response:
```json
{
                    'success': True,
                    'created': 5
}
```
4. POST /add-menu
Description: Adds a new menu item to the database.
Request Arguments: JSON object with name, price, description, available, and restaurant_id.
Example:

```json
{
    "name": "Cheeseburger",
    "price": 10,
    "description": "A delicious cheeseburger with lettuce, tomato, and cheese.",
    "available": true,
    "restaurant_id": 1
}
```
Success response:
```json
{
                    'success': True,
                    'created': 10
}
```

5. PATCH /restaurants/<int:restaurant_id>
Description: Updates the details of an existing restaurant.
Request Arguments: JSON object with any of the fields name, address, phone_number, or email to update.
Example: /restaurants/1

```json
{
        "address": "123 Pasta St",
        "email": "contact@italianbistro.com",
        "id": 1,
        "name": "New name modified here",
        "phone_number": "555-1234"
}
```

Error Response if restaurant id is not found:

```json
{
    "success": False,
    "error": "Restaurant not found"
}
```


6. DELETE /restaurants/<int:restaurant_id>
Description: Deletes a restaurant from the database.
Request Arguments: None
Returns: A JSON object indicating success and a message.
Example:

```json
{
    "success": True,
    "message": "Restaurant deleted successfully"
}
```

Error Response if restaurant id is not found:

```json
{
    "success": False,
    "error": "Restaurant not found"
}
```

