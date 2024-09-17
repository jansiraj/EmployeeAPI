from copy import deepcopy
import unittest
import json

import main
from copy import deepcopy

BASE_URL = 'http://127.0.0.1:8000'
valid_input = {"email": "jansiraj290594@gmail.com", "age": 27, "employee_id": 5, 
                    "position": "Junior Developer", "name": "jansiraj"}


class TestFlaskApi(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()
        self.secrets = {"APIKey": "abc123def456ghi789jkl012mno345pqr678stuv901wxz234"}
        self.app.testing = True

    def test_post_success_response(self):
        # valid: all required fields, age and employee_id takes int
        api_url = BASE_URL + "/createEmployee"
        response = self.app.post(api_url,
                                 data=json.dumps(valid_input),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Employee details created Successfully")
        delete_url = BASE_URL + "/deleteEmployee/5"
        self.app.delete(delete_url)

    def test_post_missing_value(self):
        # missing value field = bad
        employee = {"age": 27, "employee_id": 5, "position": "Junior Developer", 
                    "name": "jansiraja"}
        api_url = BASE_URL + "/createEmployee"
        response = self.app.post(api_url,
                                 data=json.dumps(employee),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_already_exits(self):
        # check already exists for employee id or email
        employee = deepcopy(valid_input)
        employee["employee_id"] = 5
        employee["email"] = "preethi@gmail.com"
        api_url = BASE_URL + "/createEmployee"
        response = self.app.post(api_url,
                                 data=json.dumps(employee),
                                 content_type='application/json')
        employee = {"email": "jansir290594@gmail.com", "age": 27, "employee_id": 5, 
                    "position": "Junior Developer", "name": "jansiraj"}
        response = self.app.post(api_url,
                                 data=json.dumps(employee),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data())
        self.assertEqual(data['message'], "Employee already exists")
        delete_url = BASE_URL + "/deleteEmployee/5"
        self.app.delete(delete_url)

    def test_post_valid_type(self):
        # age and employee_id field cannot take str
        api_url = BASE_URL + "/createEmployee"
        employee = {"email": "arjith@gmail.com", "age": "27", "employee_id": "2", 
                    "position": "Junior Developer", "name": "jansiraj"}
        response = self.app.post(api_url,
                                 data=json.dumps(employee),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
    def test_get_all(self):
        api_url = BASE_URL + "/getEmployeesAll"
        response = self.app.get(api_url)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "Successfully fetched all Employee details")

    def test_get_one(self):
        employee = deepcopy(valid_input)
        employee["employee_id"] = 6
        employee["email"] = "preethi@gmail.com"
        api_url = BASE_URL + "/createEmployee"
        response = self.app.post(api_url,
                                 data=json.dumps(employee),
                                 content_type='application/json')
        api_url = BASE_URL + "/getEmployee/6"
        response = self.app.get(api_url)
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], "Successfully fetched Employee detail")
        delete_url = BASE_URL + "/deleteEmployee/6"
        self.app.delete(delete_url)

    def test_update(self):
        employee = deepcopy(valid_input)
        employee["employee_id"] = 7
        employee["email"] = "preethijk@gmail.com"
        api_url = BASE_URL + "/createEmployee"
        response = self.app.post(api_url,
                                 data=json.dumps(employee),
                                 content_type='application/json')
        update_detail = {"age": 40}
        api_url = BASE_URL + "/updateEmployee/7"
        response = self.app.patch(api_url,
                                data=json.dumps(update_detail),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        delete_url = BASE_URL + "/deleteEmployee/7"
        self.app.delete(delete_url)

    def test_update_error(self):
        # age field cannot take str
        employee = deepcopy(valid_input)
        employee["employee_id"] = 8
        employee["email"] = "akvsjkm@gmail.com"
        api_url = BASE_URL + "/createEmployee"
        response = self.app.post(api_url,
                                 data=json.dumps(employee),
                                 content_type='application/json')
        update_detail = {"age": 'string'}
        api_url = BASE_URL + "/updateEmployee/8"
        response = self.app.patch(api_url,
                                data=json.dumps(update_detail),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        delete_url = BASE_URL + "/deleteEmployee/8"
        self.app.delete(delete_url)

    def test_delete(self):
        employee = deepcopy(valid_input)
        employee["employee_id"] = 9
        employee["email"] = "akvsjkm@gmail.com"
        api_url = BASE_URL + "/createEmployee"
        response = self.app.post(api_url,
                                 data=json.dumps(employee),
                                 content_type='application/json')
        api_url = BASE_URL + "/deleteEmployee/9"
        response = self.app.delete(api_url)
        self.assertEqual(response.status_code, 200)

    def test_delete_error(self):
        print("hello")
        api_url = BASE_URL + "/deleteEmployee/10"
        response = self.app.delete(api_url)
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
