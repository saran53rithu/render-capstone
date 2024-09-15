import os
from flask import Flask, jsonify, request
from models import db, Restaurant, Menu
from flask_cors import CORS
from auth import AuthError, requires_auth

# Initialize Flask app
app = Flask(__name__)

database_path = os.environ['DATABASE_URL']
# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = database_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object
db.init_app(app)


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


@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
