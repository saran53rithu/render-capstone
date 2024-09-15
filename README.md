# CAPSTONE PROJECT - RENDER APP

## Restaurant Management System Application

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
3. Restaurant worker

Restaurant owner has all access whereas restaurant worker can only view restaurant details, menu details and add new menu

### API Endpoints:

Restaurant Endpoints:

GET /restaurants: Lists all restaurants.
POST /add-restaurant: Adds a new restaurant.
PATCH /restaurants/<int:restaurant_id>: Updates details of an existing restaurant.
DELETE /restaurants/<int:restaurant_id>: Deletes a specific restaurant.

Menu Endpoints:

GET /menus: Lists all menu items.
POST /add-menu: Adds a new menu item.

GET '/restaurants'
Fetches the list of restaurants
Request Arguments: None
Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.
Example: curl http://localhost:5000/categories

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
