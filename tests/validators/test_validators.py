from unittest import mock

from sqlalchemy.exc import SQLAlchemyError
from tests.fixtures import *
from faker import Faker
from src.validators.validators import validate_token, validate_dates, CreateRouteSchema, validate_schema, \
    validate_flight_id


class TestValidators():
    # Declaración constantes
    dataFactory = Faker()
    Faker.seed(0)

    def set_up(self):
        self.flightId = self.dataFactory.word(ext_word_list=['abc', 'def', 'ghi', 'jkl'])
        self.sourceAirportCode = ''.join(self.dataFactory.random_choices(elements='ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=3))
        self.sourceCountry = self.dataFactory.country()
        self.destinyAirportCode = ''.join(self.dataFactory.random_choices(elements='ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=3))
        self.destinyCountry = self.dataFactory.country()
        self.bagCost = self.dataFactory.unique.pyint(max_value=1000)
        self.plannedStartDate = self.dataFactory.date_time_between(start_date='+5d', end_date='+6d').strftime(
            '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        self.plannedEndDate = self.dataFactory.date_time_between(start_date='+1d', end_date='+2d').strftime(
            '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        self.data = {
            "flightId": f"{self.flightId}",
            "sourceAirportCode": f"{self.sourceAirportCode}",
            "sourceCountry": f"{self.sourceCountry}",
            "destinyAirportCode": f"{self.destinyAirportCode}",
            "destinyCountry": f"{self.destinyCountry}",
            "bagCost": self.bagCost,
            "plannedStartDate": self.plannedStartDate,
            "plannedEndDate": self.plannedEndDate
        }

    def test_validate_dates_bad(self):
        self.set_up()
        assert validate_dates(self.plannedStartDate, self.plannedEndDate) == True

    def test_validate_dates_exception(self):
        self.set_up()
        try:
            validate_dates(self.plannedStartDate, '')
        except Exception as e:
            assert e.code == 412

    def test_validate_schema_bad_dates(self):
        self.set_up()
        try:
            validate_schema(self.data, CreateRouteSchema)
        except Exception as e:
            assert e.code == 412

    def test_validate_token_missing_token(self):
        headers = {}
        try:
            validate_token(headers)
        except Exception as e:
            assert e.code == 403
    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code

            def json(self):
                return self.json_data
        if kwargs['headers']['Authorization'] == 'Bearer 0':
            return MockResponse({}, 401)
        elif kwargs['headers']['Authorization'] == 'Bearer ':
            return MockResponse({""}, 403)

        return MockResponse(None, 200)

    # We patch 'requests.get' with our own method. The mock object is passed in to our test case method.
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_validators_invalid_token(self, mock_get):
        # Assert requests.get calls
        headers = {'Content-Type': 'application/json'}
        headers.update({'Authorization': 'Bearer 0'})
        try:
            response = validate_token(headers)
        except Exception as e:
            assert e.code == 401

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_validators_missing_token(self, mock_get):
        # Assert requests.get calls
        headers = {'Content-Type': 'application/json'}
        headers.update({'Authorization': 'Bearer '})
        try:
            response = validate_token(headers)
        except Exception as e:
            assert e.code == 403

    def mocked_sql_exception(*args, **kwargs):
        class MockException:
            def __init__(self, msg):
                self.msg = msg

            def json(self):
                return self.msg

        return MockException(SQLAlchemyError)

    @mock.patch('src.models.model.Routes.query.filter', side_effect=mocked_sql_exception)
    def test_validators_validate_fligth_id_exeption(self, mock_get):
        # Assert Routes.query
        try:
            validate_flight_id('')
        except Exception as e:
            assert e.code == 500

    @patch('src.models.model.Routes')
    def test_validate_flight_id_sqlalchemy_error(self, mock_query):
        # Set up
        mock_query.query.side_effect = SQLAlchemyError()
        try:
            validate_flight_id("AA001")
        except Exception as e:
            assert e.code == 500
