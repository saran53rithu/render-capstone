import unittest
from app import app
from models import db
import json

class FlaskAppTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up the Flask app and test database."""
        cls.app = app
        cls.client = cls.app.test_client()
        cls.client.testing = True
        cls.restaurant_owner_header = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imtlc2RvaXUwVHdfM2xRMEVrTnNTLSJ9.eyJpc3MiOiJodHRwczovL2Rldi04MG43b3Q1MGo2YnQ0MzBqLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmQ3NGQ3MjIzNjA3OGU0NTNmYjYzYjYiLCJhdWQiOiJyZW5kZXIiLCJpYXQiOjE3MjYzMDc3MTgsImV4cCI6MTcyNjMzNjUxOCwic2NvcGUiOiIiLCJhenAiOiJSTVRybGw4U3BFcVJTTkMxN0JnUWFLMm9wV0p1VmxtcyIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpyZXN0YXVyYW50cy1kZXRhaWwiLCJnZXQ6bWVudS1kZXRhaWwiLCJnZXQ6cmVzdGF1cmFudHMtZGV0YWlsIiwicG9zdDptZW51LWRldGFpbCIsInBvc3Q6cmVzdGF1cmFudHMtZGV0YWlsIiwidXBkYXRlOnJlc3RhdXJhbnRzLWRldGFpbCJdfQ.SMkStOIl75g6diuMXYrM8KBgQ0fTNTWOU0Chzza5wFFO55ASc2DKswK1es3vGQloBhTTzY2iVhYZMuVseohdf2GYLu_kHmXI7ZZNQZhWbtoJY5X6GTO3OMFkuzuFKclUv73JsUuB8EGVuAYoXIxnxuP8e6Cj-XuBpK9dldwaFUmo1yW_AUImM8o5BrEp5ku6UfA93km6NDPTu5YRcVtWT6MplUO-DW7Zc3xdUZAlp28RHxmBWCyoroMKMkP_yakf0DJAeG_3QR567jLys_TmIdO1YpMLiGiIZmvKepunRCEJBCjz6jDGigRAxsiUXjnzJBHqx5R5aNKij8GEdEoXcA'}
        cls.restaurant_worker = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imtlc2RvaXUwVHdfM2xRMEVrTnNTLSJ9.eyJpc3MiOiJodHRwczovL2Rldi04MG43b3Q1MGo2YnQ0MzBqLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmQ3NGQ3MjIzNjA3OGU0NTNmYjYzYjYiLCJhdWQiOiJyZW5kZXIiLCJpYXQiOjE3MjYzMTE3NjQsImV4cCI6MTcyNjM0MDU2NCwic2NvcGUiOiIiLCJhenAiOiJSTVRybGw4U3BFcVJTTkMxN0JnUWFLMm9wV0p1VmxtcyIsInBlcm1pc3Npb25zIjpbImdldDptZW51LWRldGFpbCIsImdldDpyZXN0YXVyYW50cy1kZXRhaWwiLCJwb3N0Om1lbnUtZGV0YWlsIl19.VKc-GNGGRvTNVxsZ_i8vWx1oyzWahcJX7ja9Y20HRakCj1xCqFR6mhzsGT4_eoLS2U4e2tb9G8gDdagMla1lFHFV2wIMP-MoVib8nwmAVCWFeSCcBfywVrBGNQx3k3fnn3aBX1OPVl8UdHkG7LOticR-SDGUh35ZDlRa0A5LKaexVOSnVVPnl9Vp8Q5-L8_7NDVS3xxI3ZDA3AvDqyZ0HPq4Ui-S9h_44rBHdYKcl9y2trf4F3KLEBTV4mln11pVA8M2BYCDAyPxuoobbyK_E4HicczMys_CKD_-gkDeXKDZuQ8UrPAVt7kEmidk8dYXa4BNCAArsLEL6svDPqw3pQ'}
        cls.invalid_token = {'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imtlc2RvaXUwVHdfM2xRMEVrTnNTLSJ9.eyJpc3MiOiJodHRwczovL2Rldi04MG43b3Q1MGo2YnQ0MzBqLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmQ3NGQ3MjIzNjA3OGU0NTNmYjYzYjYiLCJhdWQiOiJyZW5kZXIiLCJpYXQiOjE3MjYyMjE3MjcsImV4cCI6MTcyNjI1MDUyNywic2NvcGUiOiIiLCJhenAiOiJSTVRybGw4U3BFcVJTTkMxN0JnUWFLMm9wV0p1VmxtcyIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpyZXN0YXVyYW50cy1kZXRhaWwiLCJnZXQ6bWVudS1kZXRhaWwiLCJnZXQ6cmVzdGF1cmFudHMtZGV0YWlsIiwicG9zdDptZW51LWRldGFpbCIsInBvc3Q6cmVzdGF1cmFudHMtZGV0YWlsIiwidXBkYXRlOnJlc3RhdXJhbnRzLWRldGFpbCJdfQ.GnqbCigvrxfPmnqmTXxswvedudcqovmXs9lvfKDij3OsDH-Lx6gxH42Gp7w37YBeE6OKB37PhcdDFOdQC3ITT7wJ08AnMDAwiy7X8KFyR1N51NaMtCRD5NMTgNCnCIF3DHHaMzW40SEwTdS2wtUMZ-PsYN8NRB4c4QquPzqYtK9dSoky1y3J-7psKqhSmszSVNZZH31PKToQjc2RRlco2BQEizOXn9LQJPhlbUlQIn_YGnvfoa8eA09aY3vgo5Myviz6HJ636eDcn4mxAV2owtjrDFx5634V3azwCTB8mMYhp88zLJuojBFwgl3d-dSlfIgv0SlgniU7yODMEzm3Fw'}


        # Create an application context to access database functions
        with cls.app.app_context():
            # Initialize the database
            db.create_all()


    def test_get_restaurants_list_without_auth0(self):
        response = self.client.get('/testing-without-auth')
        self.assertEqual(response.status_code, 200)


    def test_get_restaurants_list_with_auth0(self):
        """Test accessing secure data with a valid token."""
        response = self.client.get('/restaurants', headers=self.restaurant_owner_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_get_menu_list_with_auth0(self):
        """Test accessing secure data with a valid token."""
        response = self.client.get('/menu', headers=self.restaurant_owner_header)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_restaurants_list_with_invalidtoken(self):
        """Test accessing secure data with a invalid token."""
        response = self.client.get('/restaurants', headers=self.invalid_token)
        self.assertEqual(response.status_code, 401)
    
    def test_get_menu_list_with_invalidtoken(self):
        """Test accessing secure data with a invalid token."""
        response = self.client.get('/menu', headers=self.invalid_token)
        self.assertEqual(response.status_code, 401)

    def test_add_restaurant_success(self):
        """Test adding a restaurant with valid data."""
        data = {
            "name": "New Restaurant",
            "address": "New Street",
            "phone_number": "123",
            "email": "new@example.com"
        }
        
        response = self.client.post('/add-restaurant', 
                                    headers=self.restaurant_owner_header,
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertIn('created', response_data)

    def test_add_restaurant_missing_fields(self):
        data = {
            "name": "New Restaurant",
        }
        
        response = self.client.post('/add-restaurant', 
                                    headers=self.restaurant_owner_header,
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], "All fields are required and cannot be empty")

    def test_add_restaurant_invalid_token(self):
        data = {
            "name": "New Restaurant",
            "address": "New Street",
            "phone_number": "123",
            "email": "new@example.com"
        }
        
        response = self.client.post('/add-restaurant', 
                                    headers=self.invalid_token,
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 401)
    
    def test_add_menu_success(self):
        data = {
            "name": "New Menu",
            "price": 12,
            "description": "new menu item",
            "available": True,
            "restaurant_id": 1
        }
        
        response = self.client.post('/add-menu', 
                                    headers=self.restaurant_owner_header,
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertIn('created', response_data)

    def test_add_menu_missing_fields(self):
        data = {
            "name": "New Menu",
 
        }
        
        response = self.client.post('/add-menu', 
                                    headers=self.restaurant_owner_header,
                                    data=json.dumps(data),
                                    content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['error'], "All fields are required and cannot be empty")

    def test_delete_restaurants_success(self):
        response = self.client.delete('/restaurants/3', headers=self.restaurant_owner_header)
        self.assertEqual(response.status_code, 500)

    def test_delete_restaurants_with_invalid_restaurant_id(self):
        response = self.client.delete('/restaurants/200', headers=self.restaurant_owner_header)
        self.assertEqual(response.status_code, 500)

    def test_update_restaurant_details(self):
        data = {
            "name": "New Menu",
            "price": 12,
            "description": "new menu item",
            "available": True,
            "restaurant_id": 1
        }
        res = self.client.patch('/restaurants/1', 
                                    headers=self.restaurant_owner_header,
                                    data=json.dumps(data),
                                    content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_update_restaurant_details_with_invalid_restaurant_id(self):
        data = {
            "name": "New Menu",
            "price": 12,
            "description": "new menu item",
            "available": True,
            "restaurant_id": 100
        }
        res = self.client.patch('/restaurants/100', 
                                    headers=self.restaurant_owner_header,
                                    data=json.dumps(data),
                                    content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_get_restaurant_details_by_worker(self):
        response = self.client.get('/restaurants', headers=self.restaurant_worker)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_restaurant_details_by_worker_unauthorised(self):
        response = self.client.delete('/restaurants/1', headers=self.restaurant_worker)
        self.assertEqual(response.status_code, 500)

    def test_get_menu_details_by_worker(self):
        response = self.client.get('/menu', headers=self.restaurant_worker)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()