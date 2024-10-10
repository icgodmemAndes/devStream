from faker import Faker
from sqlalchemy.exc import SQLAlchemyError

from src.commands.reset import ResetRoutes
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

    # Función que elimina data de tabla route
    def test_reset(self):
        # Eliminar route
        self.set_up()
        result = ResetRoutes().execute()
        assert result is None
        self.tearDown()
    @patch('src.models.model.db.session')
    def test_reset_route_exception(self, mock_session):
        # Set up
        mock_session.query.side_effect = SQLAlchemyError()
        # Instantiate the command
        command = ResetRoutes()

        # Execute & Assert
        try:
            command.execute()
        except Exception as e:
            assert e.code == 500
        self.tearDown()