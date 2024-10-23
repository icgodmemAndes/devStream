from unittest.mock import patch, MagicMock
from flask import Flask
from src.blueprints.mail_bp import mail_blueprint


class TestGetBlacklist():

    def setup_method(self):
        # Set up a Flask test client
        self.application = Flask(__name__)
        app_context = self.application.app_context()
        app_context.push()
        self.application.register_blueprint(mail_blueprint)

    @patch('src.blueprints.mail_bp.db')
    def test_query_blacklist_false(self, mock_db):
        # Set up
        mock_db.session.query().filter_by().one_or_none.return_value = None
        headers = {'Authorization': 'Bearer api_secret'}

        with self.application.test_client() as test_client:
            self.response = test_client.get('/blacklists/jazzjhon@gmail.com', headers=headers)
            assert self.response.status_code == 200
            assert self.response.json == {
                'is_blocked': False,
                'blocked_reason': ''
            }

    @patch('src.blueprints.mail_bp.db')
    def test_query_blacklist_true(self, mock_db):
        # Set up
        mock_mail_blocked = MagicMock()
        mock_mail_blocked.email = 'test@example.com'
        mock_mail_blocked.blocked_reason = 'spam'
        mock_db.session.query().filter_by().one_or_none.return_value = mock_mail_blocked
        headers = {'Authorization': 'Bearer api_secret'}

        with self.application.test_client() as test_client:
            self.response = test_client.get('/blacklists/test@example.com', headers=headers)
            assert self.response.status_code == 200
            assert self.response.json == {
                'is_blocked': True,
                'blocked_reason': 'spam'
            }
