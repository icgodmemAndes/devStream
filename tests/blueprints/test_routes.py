from unittest.mock import patch, MagicMock

from src.blueprints.resources import validate_token
from src.main import app
import json
from unittest import mock

from faker import Faker
from src.models.model import Routes, db


class TestRoutes():
  # Declaración constantes
  dataFactory = Faker()

  # Función que genera data del usuario
  def setup_method(self):
    db.session.rollback()
    Routes.query.delete()
    self.flightId = str(self.dataFactory.unique.pyint(max_value=9999))
    self.flightIdSecond = str(self.dataFactory.unique.pyint(max_value=9999))
    self.sourceAirportCode = ''.join(self.dataFactory.random_choices(elements='ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=3))
    self.sourceCountry = self.dataFactory.country()
    self.destinyAirportCode = ''.join(self.dataFactory.random_choices(elements='ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=3))
    self.destinyCountry = self.dataFactory.country()
    self.bagCost = self.dataFactory.unique.pyint(max_value=1000)
    self.plannedStartDate = self.dataFactory.date_time_between(start_date='+2d', end_date='+4d').strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    self.plannedEndDate = self.dataFactory.date_time_between(start_date='+5d', end_date='+10d').strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    self.data = {
      "flightId": f"{self.flightId}",
      "sourceAirportCode": f"{self.sourceAirportCode}",
      "sourceCountry": f"{self.sourceCountry}",
      "destinyAirportCode": f"{self.destinyAirportCode}",
      "destinyCountry": f"{self.destinyCountry}",
      "bagCost": self.bagCost,
      "plannedStartDate": f"{self.plannedStartDate}",
      "plannedEndDate": f"{self.plannedEndDate}"
    }

    self.new_route = Routes(
      flightId=self.flightIdSecond,
      sourceAirportCode=self.sourceAirportCode,
      sourceCountry=self.sourceCountry,
      destinyAirportCode=self.destinyAirportCode,
      destinyCountry=self.destinyCountry,
      bagCost=self.bagCost,
      plannedStartDate=self.plannedStartDate,
      plannedEndDate=self.plannedEndDate
    )
    db.session.add(self.new_route)
    db.session.commit()
    self.idOne = self.new_route.id
    self.usuario_token_valid = 'Bearer 123'

  def tearDown(self):
      db.session.rollback()
      Routes.query.delete()
  # Función que crea una route

  def test_reset_users(self):
    # Reset tabla Routes
    data = {}
    with app.test_client() as test_client:
      response = test_client.post(
        '/routes/reset', json=data
      )
      response_json = json.loads(response.data)
    assert response.status_code == 200
    assert 'msg' in response_json
    assert response_json['msg'] == 'Todos los datos fueron eliminados'

  # Función que valida el estado del servidor
  def test_health_check(self):
    # Reset tabla usuarios
    with app.test_client() as test_client:
      response = test_client.get(
        '/routes/ping'
      )
      data = str(response.data)
    assert response.status_code == 200
    assert 'pong' in data

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

    return MockResponse({}, 200)

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

  @patch('requests.get')
  def action_post_routes(self, mock_get):
    # Set up the mock response for invalid token
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "ok"}
    mock_get.return_value = mock_response
    token = self.usuario_token_valid
    data_route = self.data
    headers = {'Content-Type': 'application/json'}
    if token:
        headers.update({'Authorization': f'Bearer {token}'})
    with app.test_client() as test_client:
      self.response = test_client.post('/routes', json=data_route, headers=headers)
      self.response_json = self.response.json


  @patch('requests.get')
  def action_post_routes_no_token(self, mock_get):
    # Set up the mock response for invalid token
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.json.return_value = {"data": "ok"}
    mock_get.return_value = mock_response
    token = None
    data_route = self.data
    headers = {'Content-Type': 'application/json'}
    if token:
        headers.update({'Authorization': f'Bearer {token}'})
    with app.test_client() as test_client:
      self.response = test_client.post('/routes', json=data_route, headers=headers)
      self.response_json = self.response.json

  def test_return_201_create_route_success(self):
    self.action_post_routes()
    assert self.response.status_code == 201

  def test_return_403_no_token(self):
    self.action_post_routes_no_token()
    assert self.response.status_code == 403

  @patch('requests.get')
  def action_get_route(self, mock_get):
    # Set up the mock response for invalid token
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "ok"}
    mock_get.return_value = mock_response
    token = self.usuario_token_valid
    query = self.flightIdSecond
    headers = {'Content-Type': 'application/json'}
    if token:
        headers.update({'Authorization': f'Bearer {token}'})
    with app.test_client() as test_client:
      self.response = test_client.get(f'/routes?flight={query}', headers=headers)
      self.response_json = self.response.json

  @patch('requests.get')
  def action_get_route_no_route(self, mock_get):
    # Set up the mock response for invalid token
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "ok"}
    mock_get.return_value = mock_response
    query = None
    token = self.usuario_token_valid
    headers = {'Content-Type': 'application/json'}
    if token:
        headers.update({'Authorization': f'Bearer {token}'})
    with app.test_client() as test_client:
      self.response = test_client.get(f'/routes?flight={query}', headers=headers)
      self.response_json = self.response.json

  @patch('requests.get')
  def action_get_routes(self, mock_get):
    # Set up the mock response for invalid token
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "ok"}
    mock_get.return_value = mock_response
    token = self.usuario_token_valid
    headers = {'Content-Type': 'application/json'}
    if token:
        headers.update({'Authorization': f'Bearer {token}'})
    with app.test_client() as test_client:
      self.response = test_client.get(f'/routes', headers=headers)
      self.response_json = self.response.json

  def test_return_200_search_routes(self):
    self.action_get_routes()
    assert self.response.status_code == 200

  def test_return_200_search_routes_with_flight_id(self):
    self.action_get_route()
    assert self.response.status_code == 200

  @patch('requests.get')
  def action_get_route_id(self, mock_get):
    # Set up the mock response for invalid token
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "ok"}
    mock_get.return_value = mock_response
    token = self.usuario_token_valid
    query = str(self.idOne)
    headers = {'Content-Type': 'application/json'}
    if token:
        headers.update({'Authorization': f'Bearer {token}'})
    with app.test_client() as test_client:
      self.response = test_client.get(f'/routes/{query}', headers=headers)
      self.response_json = self.response.json

  def test_return_200_search_routes_with_id(self):
    self.action_get_route_id()
    assert self.response.status_code == 200

  @patch('requests.get')
  def action_delete_route_id(self, mock_get):
    # Set up the mock response for invalid token
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "ok"}
    mock_get.return_value = mock_response
    token = self.usuario_token_valid
    query = str(self.idOne)
    headers = {'Content-Type': 'application/json'}
    if token:
        headers.update({'Authorization': f'Bearer {token}'})
    with app.test_client() as test_client:
      self.response = test_client.delete(f'/routes/{query}', headers=headers)
      self.response_json = self.response.json

  @patch('requests.get')
  def action_delete_route_id_bad(self, mock_get):
    # Set up the mock response for invalid token
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "ok"}
    mock_get.return_value = mock_response
    token = self.usuario_token_valid
    query = str(self.flightId)
    headers = {'Content-Type': 'application/json'}
    if token:
        headers.update({'Authorization': f'Bearer {token}'})
    with app.test_client() as test_client:
      self.response = test_client.delete(f'/routes/{query}', headers=headers)
      self.response_json = self.response.json

  def test_return_200_delete_routes_with_id(self):
    self.action_delete_route_id()
    assert self.response.status_code == 200

  def test_return_200_delete_routes_with_id_bad_request(self):
    print(self.idOne)
    self.action_delete_route_id_bad()
    assert self.response.status_code == 400