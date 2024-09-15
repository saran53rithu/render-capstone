import os
from flask import Flask, jsonify, request
from models import db, Restaurant, Menu, setup_db
from flask_cors import CORS
from auth.auth import AuthError, requires_auth

# referenced from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/9e4f7f45-c341-456c-aa37-ce4d675acd9d/concepts/001a705d-06f9-472b-b2e8-b8d00e8e0372?lesson_tab=lesson

def create_app():
    app = Flask(__name__)
    database_path = os.environ['DATABASE_URL']
    setup_db(app, database_path=database_path)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

# referenced from endpoint implementation https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/9e4f7f45-c341-456c-aa37-ce4d675acd9d/concepts/c8385f51-3e6b-42be-afdb-419840f2fcaf?lesson_tab=lesson
#Also from https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/3_Testing_Review/backend/flaskr/__init__.py  
    @app.route('/testing-without-auth', methods=['GET'])
    def test_restaurants():
        try:
            restaurants = Restaurant.query.all()
            return jsonify([{
                'id': r.id,
                'name': r.name,
                'address': r.address,
                'phone_number': r.phone_number,
                'email': r.email
            } for r in restaurants])
        except Exception as e:
            return jsonify({
                "success": False,
                "error": "An error occurred while fetching the restaurant details"
            }), 422

# referenced from endpoint implementation https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/9e4f7f45-c341-456c-aa37-ce4d675acd9d/concepts/c8385f51-3e6b-42be-afdb-419840f2fcaf?lesson_tab=lesson and auth0 reference from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/3bd56b2d-7a3f-4aff-90f8-842eec9071a9/concepts/8c8da3d7-8591-4d70-b570-76e6cda7c8b5?lesson_tab=lesson
#Also from https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/3_Testing_Review/backend/flaskr/__init__.py

    @app.route('/restaurants', methods=['GET'])
    @requires_auth('get:restaurants-detail')
    def get_restaurants(payload):
        try:
            restaurants = Restaurant.query.all()
            return jsonify([{
                'id': r.id,
                'name': r.name,
                'address': r.address,
                'phone_number': r.phone_number,
                'email': r.email
            } for r in restaurants])
        except Exception as e:
            return jsonify({
                "success": False,
                "error": "An error occurred while fetching the restaurant details"
            }), 422

# referenced from endpoint implementation https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/9e4f7f45-c341-456c-aa37-ce4d675acd9d/concepts/c8385f51-3e6b-42be-afdb-419840f2fcaf?lesson_tab=lesson and auth0 reference from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/3bd56b2d-7a3f-4aff-90f8-842eec9071a9/concepts/8c8da3d7-8591-4d70-b570-76e6cda7c8b5?lesson_tab=lesson
#Also from https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/3_Testing_Review/backend/flaskr/__init__.py

    @app.route('/menu', methods=['GET'])
    @requires_auth('get:menu-detail')
    def get_menu(payload):
        try:
            menus = Menu.query.all()
            return jsonify([{
                'id': m.id,
                'name': m.name,
                'price': str(m.price),
                'description': m.description,
                'available': m.available,
                'restaurant_id': m.restaurant_id
            } for m in menus])
        except Exception as e:
            return jsonify({
                "success": False,
                "error": "An error occurred while fetching the menu items"
            }), 422

# referenced from endpoint implementation https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/9e4f7f45-c341-456c-aa37-ce4d675acd9d/concepts/c8385f51-3e6b-42be-afdb-419840f2fcaf?lesson_tab=lesson and auth0 reference from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/3bd56b2d-7a3f-4aff-90f8-842eec9071a9/concepts/8c8da3d7-8591-4d70-b570-76e6cda7c8b5?lesson_tab=lesson
#Also from https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/3_Testing_Review/backend/flaskr/__init__.py

    @app.route('/add-restaurant', methods=['POST'])
    @requires_auth('post:restaurants-detail')
    def add_restaurant(payload):
        body = request.get_json()
        new_name = body.get("name", None)
        new_address = body.get("address", None)
        new_phone_number = body.get("phone_number", None)
        new_email = body.get("email", None)

        if not all([new_name, new_address, new_phone_number, new_email]):
            return jsonify({
                "success": False,
                "error": "All fields are required and cannot be empty"
            }), 400

        restaurants = Restaurant.query.all()

        try:
            restaurant = Restaurant(name=new_name, address=new_address, phone_number=new_phone_number, email=new_email)
            db.session.add(restaurant)
            db.session.commit()

            return jsonify(
                {
                    'success': True,
                    'created': restaurant.id
                }
            )

        except Exception as e:
            return jsonify({
                "success": False,
                "error": "An error occurred while adding the new restaurant details"
            }), 422

# referenced from endpoint implementation https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/9e4f7f45-c341-456c-aa37-ce4d675acd9d/concepts/c8385f51-3e6b-42be-afdb-419840f2fcaf?lesson_tab=lesson and auth0 reference from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/3bd56b2d-7a3f-4aff-90f8-842eec9071a9/concepts/8c8da3d7-8591-4d70-b570-76e6cda7c8b5?lesson_tab=lesson
#Also from https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/3_Testing_Review/backend/flaskr/__init__.py

    @app.route('/add-menu', methods=['POST'])
    @requires_auth('post:menu-detail')
    def add_menu(payload):
        body = request.get_json()
        new_name = body.get("name", None)
        new_price = body.get("price", None)
        new_description = body.get("description", None)
        new_available = body.get("available", None)
        new_restaurant_id = body.get("restaurant_id", None)

        if not all([new_name, new_price, new_description, new_available, new_restaurant_id]):
            return jsonify({
                "success": False,
                "error": "All fields are required and cannot be empty"
            }), 400

        menus = Menu.query.all()

        try:
            restaurant = Restaurant.query.get(new_restaurant_id)
            if not restaurant:
                return jsonify({
                    "success": False,
                    "error": "Restaurant with the given ID does not exist"
                }), 404
            menu = Menu(name=new_name, price=new_price, description=new_description, available=new_available, restaurant_id=new_restaurant_id)
            db.session.add(menu)
            db.session.commit()

            return jsonify(
                {
                    'success': True,
                    'created': menu.id
                }
            )
        except Exception as e:
            return jsonify({
                "success": False,
                "error": "An error occurred while creating the menu item"
            }), 422

# referenced from endpoint implementation https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/9e4f7f45-c341-456c-aa37-ce4d675acd9d/concepts/c8385f51-3e6b-42be-afdb-419840f2fcaf?lesson_tab=lesson and auth0 reference from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/3bd56b2d-7a3f-4aff-90f8-842eec9071a9/concepts/8c8da3d7-8591-4d70-b570-76e6cda7c8b5?lesson_tab=lesson
#Also from https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/3_Testing_Review/backend/flaskr/__init__.py

    @app.route('/restaurants/<int:restaurant_id>', methods=['PATCH'])
    @requires_auth('update:restaurants-detail')
    def update_restaurant(payload, restaurant_id):

        restaurant = Restaurant.query.get(restaurant_id)
        if restaurant is None:
            return jsonify({
                "success": False,
                "error": "Restaurant not found"
            }), 404

        body = request.get_json()
        new_name = body.get("name", None)
        new_address = body.get("address", None)
        new_phone_number = body.get("phone_number", None)
        new_email = body.get("email", None)

        if 'name' in body:
            restaurant.name = body['name']
        if 'address' in body:
            restaurant.address = body['address']
        if 'phone_number' in body:
            restaurant.phone_number = body['phone_number']
        if 'email' in body:
            restaurant.email = body['email']

        try:
            db.session.commit()
            return jsonify({
                'success': True,
                'id': restaurant.id,
                'name': restaurant.name,
                'address': restaurant.address,
                'phone_number': restaurant.phone_number,
                'email': restaurant.email
            }), 200

        except Exception as e:
            return jsonify({
                "success": False,
                "error": "An error occurred while updating the restaurant details"
            }), 422

# referenced from endpoint implementation https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/9e4f7f45-c341-456c-aa37-ce4d675acd9d/concepts/c8385f51-3e6b-42be-afdb-419840f2fcaf?lesson_tab=lesson and auth0 reference from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0039/lessons/3bd56b2d-7a3f-4aff-90f8-842eec9071a9/concepts/8c8da3d7-8591-4d70-b570-76e6cda7c8b5?lesson_tab=lesson
#Also from https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/3_Testing_Review/backend/flaskr/__init__.py

    @app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
    @requires_auth('delete:restaurants-detail')
    def delete_restaurant(payload, restaurant_id):
        try:
            restaurant = Restaurant.query.get(restaurant_id)
            print(restaurant)
            if not restaurant:
                return jsonify({
                    "success": False,
                    "error": "Restaurant not found"
                }), 404

            db.session.delete(restaurant)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Restaurant deleted successfully'
            }), 200

        except Exception as e:
            return jsonify({
                "success": False,
                "error": "An error occurred while deleting the restaurant details"
            }), 422


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Not found'
        }), 404

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
