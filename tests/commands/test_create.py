from src.commands.create import CreateRoute
from faker import Faker

from src.models.model import Routes
from tests.fixtures import *

# Clase que contiene la logica de las pruebas del servicio
class TestRoute():
    # Declaración constantes
    dataFactory = Faker()
    Faker.seed(0)

    # Función que genera data del route
    def set_up(self):
        db.session.rollback()
        Routes.query.delete()
        self.flightId = self.dataFactory.word(ext_word_list=['abc', 'def', 'ghi', 'jkl'])
        self.flightIdSecond = self.dataFactory.word(ext_word_list=['Mno', 'Pqr', 'Stu', 'Vwx'])
        self.sourceAirportCode = ''.join(self.dataFactory.random_choices(elements='ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=3))
        self.sourceCountry = self.dataFactory.country()
        self.destinyAirportCode = ''.join(self.dataFactory.random_choices(elements='ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=3))
        self.destinyCountry = self.dataFactory.country()
        self.bagCost = self.dataFactory.unique.pyint(max_value=1000)
        self.plannedStartDate = self.dataFactory.date_time_between(start_date='+2d', end_date='+4d').strftime(
            '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        self.plannedEndDate = self.dataFactory.date_time_between(start_date='+5d', end_date='+10d').strftime(
            '%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        self.route = Routes(flightId=self.flightId,
                            sourceAirportCode=self.sourceAirportCode,
                            sourceCountry=self.sourceCountry,
                            destinyAirportCode=self.destinyAirportCode,
                            destinyCountry=self.destinyCountry,
                            bagCost=self.bagCost,
                            plannedStartDate=self.plannedStartDate,
                            plannedEndDate=self.plannedEndDate)
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
        self.dataSecond = {
            "flightId": f"{self.flightIdSecond}",
            "sourceAirportCode": f"{self.sourceAirportCode}",
            "sourceCountry": f"{self.sourceCountry}",
            "destinyAirportCode": f"{self.destinyAirportCode}",
            "destinyCountry": f"{self.destinyCountry}",
            "bagCost": self.bagCost,
            "plannedStartDate": self.plannedStartDate,
            "plannedEndDate": self.plannedEndDate
        }

    def tearDown(self):
        db.session.rollback()
        Routes.query.delete()

    # Función que crea una route

    # Función que valida la creación exitosa de un usuario
    def test_create_new_route(self):
        # Creación route
        self.set_up()
        result = CreateRoute(self.data).execute()

        assert result is not None
        self.tearDown()

    # Función que valida la creación de un route ya registrado
    def test_existing_route_creation(self):
        try:
            # Creación route
            self.set_up()
            result = CreateRoute(self.data).execute()
            assert result is not None
            #db.session.commit(self.route)
            # Creación route duplicado
            CreateRoute(self.data).execute()
        except Exception as e:
            assert e.code == 412
        self.tearDown()

    # Función que valida la creación de un usuario cuando se envia un request invalido
    def test_create_route_bad_request(self):
        try:
            # Creación route
            self.set_up()
            data = {
                "some": f"{self.flightId}"
            }
            # Creación route con data incompleta
            result = CreateRoute(data).execute()
        except Exception as e:
            assert e.code == 400
        self.tearDown()
