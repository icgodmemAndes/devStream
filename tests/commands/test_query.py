import uuid


from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from src.commands.query import QueryRouteByFlight, QueryRouteById, CheckFlightIdFormat, CheckIdFormat
from src.errors.errors import ApiError
from src.models.model import Routes
from tests.fixtures import *

# Clase que contiene la logica de las pruebas del servicio
class TestRoute():
    # Declaración constantes
    dataFactory = Faker()
    Faker.seed(0)
    data = {}

    # Función que genera data del route
    def set_up(self):
        db.session.rollback()
        Routes.query.delete()
        self.flightId = self.dataFactory.word(ext_word_list=['abc', 'def', 'ghi', 'jkl'])
        self.flightIdInvalid = self.dataFactory.word(ext_word_list=['a', 'b', 'c', 'd'])
        self.flightIdTwo = self.dataFactory.word(ext_word_list=['mno', 'pqr', 'stu', 'vwx'])
        self.sourceAirportCode = ''.join(self.dataFactory.random_choices(elements='ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=3))
        self.sourceCountry = self.dataFactory.country()
        self.destinyAirportCode = ''.join(self.dataFactory.random_choices(elements='ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=3))
        self.destinyCountry = self.dataFactory.country()
        self.bagCost = self.dataFactory.unique.pyint(max_value=1000)
        self.plannedStartDate = self.dataFactory.future_datetime(end_date='+1d').strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        self.plannedEndDate = self.dataFactory.future_datetime(end_date='+30d').strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        self.new_route = Routes(
            flightId=self.flightId,
            sourceAirportCode=self.sourceAirportCode,
            sourceCountry=self.sourceCountry,
            destinyAirportCode=self.destinyAirportCode,
            destinyCountry=self.destinyCountry,
            bagCost=self.bagCost,
            plannedStartDate=self.plannedStartDate,
            plannedEndDate=self.plannedEndDate
        )
        self.new_route_second = Routes(
            flightId=self.flightIdTwo,
            sourceAirportCode=self.sourceAirportCode,
            sourceCountry=self.sourceCountry,
            destinyAirportCode=self.destinyAirportCode,
            destinyCountry=self.destinyCountry,
            bagCost=self.bagCost,
            plannedStartDate=self.plannedStartDate,
            plannedEndDate=self.plannedEndDate
        )
        db.session.add(self.new_route)
        db.session.add(self.new_route_second)
        db.session.commit()
        self.idOne = self.new_route.id

    def tearDown(self):
        db.session.rollback()
        Routes.query.delete()

    # Función que valida la busqueda todas las routes
    def test_query_all_route(self):
        # Buscar route
        self.set_up()
        result = QueryRouteByFlight(None).execute()
        assert len(result) == 2
        self.tearDown()

    # Función que valida la busqueda de un route
    def test_query_one_route(self):
        # Buscar route
        self.set_up()
        result = QueryRouteByFlight(self.flightIdTwo).execute()
        assert result[0]['flightId'] == self.flightIdTwo
        self.tearDown()

    # Función que valida la busqueda de un route ya registrado
    def test_query_route_id(self):
        # Buscar route con ID
        self.set_up()
        result = QueryRouteById(self.idOne).execute()
        assert uuid.UUID(result['id']) == self.idOne
        self.tearDown()

    # Función que valida la busqueda de un route no existe
    def test_query_route_id_not_exist(self):
        # Buscar route con ID
        self.set_up()
        try:
            result = QueryRouteById(uuid.uuid4()).execute()

        except Exception as e:
            assert e.code == 404
        self.tearDown()

    # Función que valida format flightId
    def test_query_flight_id_format_valid(self):
        # Validar formato
        self.set_up()
        result = CheckFlightIdFormat(self.flightId).execute()
        assert result is None
        self.tearDown()

    # Función que valida format flightId no valido
    def test_query_flight_id_format_invalid(self):
        # Validar formato
        self.set_up()
        try:
            result = CheckFlightIdFormat(self.flightIdInvalid).execute()

        except Exception as e:
            assert e.code == 400

    # Función que valida format id
    def test_query_id_format_valid(self):
        # Validar formato
        self.set_up()
        result = CheckIdFormat(str(self.idOne)).execute()
        assert result is None

    # Función que valida format id no valido
    def test_query_id_format_invalid(self):
        # Validar formato
        self.set_up()
        try:
            result = CheckIdFormat(self.flightIdInvalid).execute()

        except Exception as e:
            assert e.code == 400

    @patch('src.models.model.Routes.query')
    def test_query_route_exception(self, mock_query):
        # Set up
        mock_query.filter.side_effect = SQLAlchemyError()
        # Instantiate the command
        command = QueryRouteByFlight("some-id")

        try:
            command.execute()
        except Exception as e:
            assert e.code == 500
        self.tearDown()
    @patch('src.models.model.Routes.query')
    def test_query_route_id_exception(self, mock_query):
        # Set up
        mock_query.filter.side_effect = SQLAlchemyError()
        # Instantiate the command
        command = QueryRouteById("some-id")

        # Execute & Assert
        try:
            command.execute()
        except Exception as e:
            assert e.code == 500
        self.tearDown()
