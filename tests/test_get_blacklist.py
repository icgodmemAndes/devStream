from unittest.mock import patch, MagicMock
from flask import Flask
from src.blueprints.mail_bp import mail_blueprint
from src.errors.errors import InvalidDataError, ApiError


class TestGetBlacklist():

    def setup_method(self):
        # Set up a Flask test client
        self.application = Flask(__name__)
        app_context = self.application.app_context()
        app_context.push()
        self.application.register_blueprint(mail_blueprint)

    @patch('src.models.mail.MailBlocked.query')
    def test_query_blacklist(self, mock_query):
        # Set up
        mock_query.filter.side_effect = {
            "email":"jazzjhon1@gmail.com",
            "app_uuid":"85482912-afc3-4147-a458-9ac4b99242bd",
            "blocked_reason":"spam"
        }
        token = 'api_secret'
        headers = {'Authorization': 'Bearer valid_token'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        with self.application.test_client() as test_client:
            self.response = test_client.get('/blacklists/jazzjhon@gmail.com', headers=headers)
            self.response_json = self.response.json