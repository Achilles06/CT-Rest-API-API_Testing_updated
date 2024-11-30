import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestEmployeeEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('models.db.session.query')
    def test_employee_valid(self, mock_query):
        # Mock database response for a valid case
        mock_query.return_value.filter_by.return_value.first.return_value = MagicMock(id=1, name='Test Data')
        response = self.app.get('/employee')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Data', response.data)

    @patch('models.db.session.query')
    def test_employee_not_found(self, mock_query):
        # Mock database response for not found case
        mock_query.return_value.filter_by.return_value.first.return_value = None
        response = self.app.get('/employee/999')  # Assume 999 is a non-existent ID
        self.assertEqual(response.status_code, 404)

    @patch('models.db.session.query')
    def test_employee_exception(self, mock_query):
        # Mock database response to raise an exception
        mock_query.side_effect = Exception('Database error')
        response = self.app.get('/employee')
        self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()
