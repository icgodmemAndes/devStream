from unittest import TestCase
from src.models.model import Routes
from sqlalchemy import exc
from faker import Faker
from tests.fixtures import *

class TestCreateRoute(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()
        # Set up the F
        # lask app and test client
        self.data_factory = Faker()
        Faker.seed(0)
        self.id = self.data_factory.uuid4()
        self.flightId = self.data_factory.word(ext_word_list=['abc', 'def', 'ghi', 'jkl'])
        self.sourceAirportCode = ''.join(self.data_factory.random_choices(elements='ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=3))
        self.sourceCountry = self.data_factory.country()
        self.destinyAirportCode = ''.join(self.data_factory.random_choices(elements='ABCDEFGHIJKLMNOPQRSTUVWXYZ', length=3))
        self.destinyCountry = self.data_factory.country()
        self.bagCost = self.data_factory.unique.random_int(min=1, max=10),
        self.plannedStartDate = self.data_factory.future_datetime(end_date='+1d')
        self.plannedEndDate = self.data_factory.future_datetime(end_date='+30d')

    def tearDown(self):
        db.session.rollback()
        Routes.query.delete()
    def test_solo_un_routes_es_creado_en_db(self):
        new_route = Routes(
            id=self.id,
            flightId=self.flightId,
            sourceAirportCode=self.sourceAirportCode,
            sourceCountry=self.sourceCountry,
            destinyAirportCode=self.destinyAirportCode,
            destinyCountry=self.destinyCountry,
            bagCost=self.bagCost,
            plannedStartDate=self.plannedStartDate,
            plannedEndDate=self.plannedEndDate
        )
        db.session.add(new_route)
        db.session.commit()

        routes_in_db = Routes.query.all()
        self.assertEqual(len(routes_in_db), 1)
        self.tearDown()

    def test_route_esperado_es_creado(self):
        new_route = Routes(
            id=self.id,
            flightId=self.flightId,
            sourceAirportCode=self.sourceAirportCode,
            sourceCountry=self.sourceCountry,
            destinyAirportCode=self.destinyAirportCode,
            destinyCountry=self.destinyCountry,
            bagCost=self.bagCost,
            plannedStartDate=self.plannedStartDate,
            plannedEndDate=self.plannedEndDate
        )
        db.session.add(new_route)
        db.session.commit()

        route_from_db = Routes.query.filter(Routes.id == self.id).first()
        self.assertEqual(route_from_db.flightId, self.flightId)
        self.tearDown()

    def test_dispara_un_error_de_integridad(self):
        first_route = Routes(
            id=self.id,
            flightId=self.flightId,
            sourceAirportCode=self.sourceAirportCode,
            sourceCountry=self.sourceCountry,
            destinyAirportCode=self.destinyAirportCode,
            destinyCountry=self.destinyCountry,
            bagCost=self.bagCost,
            plannedStartDate=self.plannedStartDate,
            plannedEndDate=self.plannedEndDate
        )
        db.session.add(first_route)
        db.session.commit()
        with self.assertRaises(exc.IntegrityError):
            route_same_fligthId = Routes(
                id=self.id,
                flightId=self.flightId,
                sourceAirportCode=self.sourceAirportCode,
                sourceCountry=self.sourceCountry,
                destinyAirportCode=self.destinyAirportCode,
                destinyCountry=self.destinyCountry,
                bagCost=self.bagCost,
                plannedStartDate=self.plannedStartDate,
                plannedEndDate=self.plannedEndDate
            )
            db.session.add(route_same_fligthId)
            db.session.commit()
        self.tearDown()
    def test_campos_no_pueden_ser_nullos(self):
        route = Routes()
        with self.assertRaises(exc.IntegrityError):
            db.session.add(route)
            db.session.commit()

        self.tearDown()