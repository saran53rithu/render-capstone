import unittest
from app import app
from models import db
import json

class FlaskAppTestCase(unittest.TestCase):

# referenced from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/c0d74496-2a4b-4dce-8cad-420bfb5c398d/concepts/e71d6e11-0c87-428a-9035-b518e277fd2f?lesson_tab=lesson and 
 #   https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/c0d74496-2a4b-4dce-8cad-420bfb5c398d/concepts/9979f45a-02ee-4a4c-8a19-dd99c0987494?lesson_tab=lesson
 #   https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/4_TDD_Review/backend/test_flaskr.py
    
    @classmethod
    def setUpClass(cls):
        """Set up the Flask app and test database."""
        cls.app = app
        cls.client = cls.app.test_client()
        cls.client.testing = True
        cls.restaurant_owner_header = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imtlc2RvaXUwVHdfM2xRMEVrTnNTLSJ9.eyJpc3MiOiJodHRwczovL2Rldi04MG43b3Q1MGo2YnQ0MzBqLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmQ3NGQ3MjIzNjA3OGU0NTNmYjYzYjYiLCJhdWQiOiJyZW5kZXIiLCJpYXQiOjE3MjYzNzEyMzAsImV4cCI6MTcyNjQwMDAzMCwic2NvcGUiOiIiLCJhenAiOiJSTVRybGw4U3BFcVJTTkMxN0JnUWFLMm9wV0p1VmxtcyIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpyZXN0YXVyYW50cy1kZXRhaWwiLCJnZXQ6bWVudS1kZXRhaWwiLCJnZXQ6cmVzdGF1cmFudHMtZGV0YWlsIiwicG9zdDptZW51LWRldGFpbCIsInBvc3Q6cmVzdGF1cmFudHMtZGV0YWlsIiwidXBkYXRlOnJlc3RhdXJhbnRzLWRldGFpbCJdfQ.g7lMT4hzM9pPCNDopfAa-IkGkAtBtUQ_uuerKcrTiR8NIl_W3giGOIZS6Kqft2wmibXVKBtyBnn_FD4LB2rW4nxJYdEpAZcAUhbD2u6Z8U8KHxqS19sCZieXXYITPlo2gyd_iIhyUXk5JOiM_gqjgG12zvDNMqjTMh9FTxKpUys0dZWK-BbGh0FT4i_RuiIX84Oteq0sPAlWk94wfQZOUaQ1sQfYl40yw222ZBtS9ba85Lw4fpCwSOGCCpdImI2GINH20cTddMYlZe843L2eYlmO5nLfKHQrRxboiErUIMiWZ17vE18mqZHelJttaBLVEhTZrSR1USrl-4vWK4d2Lg'}
        cls.restaurant_worker = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imtlc2RvaXUwVHdfM2xRMEVrTnNTLSJ9.eyJpc3MiOiJodHRwczovL2Rldi04MG43b3Q1MGo2YnQ0MzBqLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmQ3NGQ3MjIzNjA3OGU0NTNmYjYzYjYiLCJhdWQiOiJyZW5kZXIiLCJpYXQiOjE3MjYzNzEwODEsImV4cCI6MTcyNjM5OTg4MSwic2NvcGUiOiIiLCJhenAiOiJSTVRybGw4U3BFcVJTTkMxN0JnUWFLMm9wV0p1VmxtcyIsInBlcm1pc3Npb25zIjpbImdldDptZW51LWRldGFpbCIsImdldDpyZXN0YXVyYW50cy1kZXRhaWwiLCJwb3N0Om1lbnUtZGV0YWlsIl19.c2Wcja_Ds4nfCkIk7ZX5LfO1YwrC0PbFVdddAhzbTO36fHbPU_fnDj6NQhYmpyXZ199lut653bXcxXOb4gbrP6VPH19JHy8AJq4ZoWX9QJTiLzKDGs08QWw_KsTAvF9IJyQfIsp9MzsqA5J-KO2rXIn8Hl7KAE_RGIzwPBKySHApHk_rMAMuiKHn1OY0_9o23oTD4PrCANaVZSPbEzP2lO5hOuRa-UhPQj0AoSr0tcjtNQaHN5lecmQa8W4W1X2-XKqQRSN9FiGxPeowvU9JrEAR_V6cXB5eG1EwcMzjN7hI-uNFdswUAKKxWfWELPBFl3WXLaSoGkeQ7H3ioWOB8A'}
        cls.invalid_token = {'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Imtlc2RvaXUwVHdfM2xRMEVrTnNTLSJ9.eyJpc3MiOiJodHRwczovL2Rldi04MG43b3Q1MGo2YnQ0MzBqLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NmQ3NGQ3MjIzNjA3OGU0NTNmYjYzYjYiLCJhdWQiOiJyZW5kZXIiLCJpYXQiOjE3MjYyMjE3MjcsImV4cCI6MTcyNjI1MDUyNywic2NvcGUiOiIiLCJhenAiOiJSTVRybGw4U3BFcVJTTkMxN0JnUWFLMm9wV0p1VmxtcyIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpyZXN0YXVyYW50cy1kZXRhaWwiLCJnZXQ6bWVudS1kZXRhaWwiLCJnZXQ6cmVzdGF1cmFudHMtZGV0YWlsIiwicG9zdDptZW51LWRldGFpbCIsInBvc3Q6cmVzdGF1cmFudHMtZGV0YWlsIiwidXBkYXRlOnJlc3RhdXJhbnRzLWRldGFpbCJdfQ.GnqbCigvrxfPmnqmTXxswvedudcqovmXs9lvfKDij3OsDH-Lx6gxH42Gp7w37YBeE6OKB37PhcdDFOdQC3ITT7wJ08AnMDAwiy7X8KFyR1N51NaMtCRD5NMTgNCnCIF3DHHaMzW40SEwTdS2wtUMZ-PsYN8NRB4c4QquPzqYtK9dSoky1y3J-7psKqhSmszSVNZZH31PKToQjc2RRlco2BQEizOXn9LQJPhlbUlQIn_YGnvfoa8eA09aY3vgo5Myviz6HJ636eDcn4mxAV2owtjrDFx5634V3azwCTB8mMYhp88zLJuojBFwgl3d-dSlfIgv0SlgniU7yODMEzm3Fw'}


        # Create an application context to access database functions
        with cls.app.app_context():
            # Initialize the database
            db.create_all()

# referenced from https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/c0d74496-2a4b-4dce-8cad-420bfb5c398d/concepts/e71d6e11-0c87-428a-9035-b518e277fd2f?lesson_tab=lesson and 
 #   https://learn.udacity.com/nanodegrees/nd0044/parts/cd0037/lessons/c0d74496-2a4b-4dce-8cad-420bfb5c398d/concepts/9979f45a-02ee-4a4c-8a19-dd99c0987494?lesson_tab=lesson
 #   https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/blob/master/4_TDD_Review/backend/test_flaskr.py
    
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
