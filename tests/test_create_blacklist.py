from unittest.mock import patch, MagicMock
from flask import Flask
from src.blueprints.mail_bp import mail_blueprint
from src.errors.errors import InvalidDataError, ApiError


class TestCreateBlacklist():

    def setup_method(self):
        # Set up a Flask test client
        self.application = Flask(__name__)
        app_context = self.application.app_context()
        app_context.push()
        self.application.register_blueprint(mail_blueprint)


    def mocked_create(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data

        return MockResponse({
            'id': '123e4567-e89b-12d3-a456-426614174000',
            'msg': 'Blacklist agregada satisfactoriamente',
            'createdAt': '2024-10-22T10:00:00'
        }, 200)

    @patch('src.blueprints.mail_bp.CreateBlacklist')
    def action_post_blacklist(self, mocked_create):

        mocked_response_create = MagicMock()
        mocked_response_create.id = '123e4567-e89b-12d3-a456-426614174000'
        mocked_response_create.msg = 'Blacklist agregada satisfactoriamente'
        mocked_response_create.createdAt = '2024-10-22T10:00:00'

        mocked_create.return_value.execute.return_value = {
            'id': '123e4567-e89b-12d3-a456-426614174000',
            'msg': 'Blacklist agregada satisfactoriamente',
            'createdAt': '2024-10-22T10:00:00'
        }
        token = 'api_secret'

        data_blacklist = {
            "email":"jazzjhon1@gmail.com",
            "appUuid":"85482912-afc3-4147-a458-9ac4b99242bd",
            "blockedReason":"spam"
        }
        headers = {'Authorization': 'Bearer valid_token'}
        if token:
            headers.update({'Authorization': f'Bearer {token}'})
        with self.application.test_client() as test_client:
            self.response = test_client.post('/blacklists', json=data_blacklist, headers=headers)
            self.response_json = self.response.json

    def test_post_blacklist(self):
        self.action_post_blacklist()
        assert self.response.status_code == 201
