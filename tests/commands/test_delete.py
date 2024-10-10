import uuid

from faker import Faker

from src.commands.delete import DeleteRouteById
from src.errors.errors import ApiError
from src.models.model import Routes
from tests.fixtures import *
from sqlalchemy.exc import SQLAlchemyError
from unittest.mock import patch

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

        db.session.add(self.new_route)
        db.session.commit()
        self.idOne = self.new_route.id

    def tearDown(self):
        db.session.rollback()
        Routes.query.delete()

    # Función que valida borrar un route
    def test_delete_one_route(self):
        # Eliminar route
        self.set_up()
        result = DeleteRouteById(str(self.idOne)).execute()
        assert result['msg'] == "el trayecto fue eliminado"
        self.tearDown()
    # Función que valida borrar un route no existente
    def test_query_route_id(self):
        # Eliminar route
        self.set_up()
        try:
            DeleteRouteById(str(uuid.uuid4())).execute()
        except Exception as e:
            assert e.code == 404
        self.tearDown()

    @patch('src.models.model.Routes.query.filter')
    def test_delete_route_exception(self, mock_query):
        # Set up
        mock_query.one_or_none.side_effect = SQLAlchemyError()
        # Instantiate the command
        command = DeleteRouteById("e3e70682--4444-a29f-6666682c07cd")

        # Execute & Assert
        try:
            command.execute()
        except Exception as e:
            assert e.code == 500
        self.tearDown()
