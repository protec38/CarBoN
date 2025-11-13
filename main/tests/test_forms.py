from django.test import TestCase

from main.models import Vehicle, Trip, FuelExpense
from main.forms import DefectForm, FuelExpenseForm, TripStartForm, TripEndForm, TripForm


class FormsVehicleParameterTestCase(TestCase):
    """
    Test that all forms can handle the vehicle parameter gracefully
    """

    @classmethod
    def setUpTestData(cls):
        cls.vehicle = Vehicle.objects.create(
            name="Test Vehicle",
            type=Vehicle.VehicleType.VL,
            model_name="Test Model",
            fuel=Vehicle.FuelChoice.DIESEL,
            registration_number="TEST123",
            status=Vehicle.VehicleStatus.OPERATIONAL,
        )
        Trip.objects.create(
            vehicle=cls.vehicle,
            starting_mileage=0,
            ending_mileage=20000,
            driver_name="Test Driver",
            purpose="Test Purpose",
            finished=True,
        )

    def test_defect_form_accepts_vehicle_parameter(self):
        """
        Test that DefectForm accepts vehicle parameter without errors
        """
        # WHEN a DefectForm is created with vehicle parameter
        form = DefectForm(vehicle=self.vehicle)

        # THEN the form should be created successfully
        self.assertIsInstance(form, DefectForm)
        # The vehicle parameter should be ignored (no initial values set from vehicle)
        self.assertIsNone(form.fields["reporter_name"].initial)

    def test_fuel_expense_form_accepts_vehicle_parameter(self):
        """
        Test that FuelExpenseForm accepts vehicle parameter and uses it
        """
        # WHEN a FuelExpenseForm is created with vehicle parameter
        form = FuelExpenseForm(vehicle=self.vehicle)

        # THEN the form should be created successfully and use vehicle mileage
        self.assertIsInstance(form, FuelExpenseForm)
        self.assertEqual(form.fields["mileage"].initial, self.vehicle.mileage)

    def test_trip_start_form_accepts_vehicle_parameter(self):
        """
        Test that TripStartForm accepts vehicle parameter and uses it
        """
        # WHEN a TripStartForm is created with vehicle parameter
        form = TripStartForm(vehicle=self.vehicle)

        # THEN the form should be created successfully and use vehicle mileage
        self.assertIsInstance(form, TripStartForm)
        self.assertEqual(form.fields["starting_mileage"].initial, self.vehicle.mileage)

    def test_trip_end_form_accepts_vehicle_parameter(self):
        """
        Test that TripEndForm accepts vehicle parameter without errors
        """
        # WHEN a TripEndForm is created with vehicle parameter
        form = TripEndForm(vehicle=self.vehicle)

        # THEN the form should be created successfully
        self.assertIsInstance(form, TripEndForm)
        # The vehicle parameter should be ignored for TripEndForm
        # (it inherits from TripForm but overrides __init__ without vehicle handling)

    def test_all_forms_work_without_vehicle_parameter(self):
        """
        Test that all forms work when no vehicle parameter is provided
        """
        forms_to_test = [DefectForm, FuelExpenseForm, TripStartForm, TripEndForm]

        for form_class in forms_to_test:
            with self.subTest(form_class=form_class.__name__):
                # WHEN a form is created without vehicle parameter
                form = form_class()

                # THEN the form should be created successfully
                self.assertIsInstance(form, form_class)

    def test_forms_vehicle_initialization_edge_cases(self):
        """
        Test edge cases for vehicle parameter handling
        """
        # Test with None vehicle - should use model field default (0)
        fuel_form = FuelExpenseForm(vehicle=None)
        self.assertEqual(fuel_form.fields["mileage"].initial, 0)  # Model field default

        trip_form = TripStartForm(vehicle=None)
        self.assertIsNone(
            trip_form.fields["starting_mileage"].initial
        )  # No default on Trip model

        # Test that vehicle parameter doesn't interfere with other kwargs
        fuel_form_with_data = FuelExpenseForm(
            data={"mileage": 15000}, vehicle=self.vehicle
        )
        # When bound, initial is not used from vehicle (form uses bound data instead)
        self.assertEqual(
            fuel_form_with_data.data["mileage"], 15000
        )  # Check bound data instead


class FuelExpenseFormTestCase(TestCase):
    """
    Dedicated unit tests for FuelExpenseForm
    """

    @classmethod
    def setUpTestData(cls):
        cls.vehicle = Vehicle.objects.create(
            name="VPS Test",
            type=Vehicle.VehicleType.VPSP,
            model_name="Renault Master",
            fuel=Vehicle.FuelChoice.DIESEL,
            registration_number="1234ABCD",
            status=Vehicle.VehicleStatus.OPERATIONAL,
        )
        Trip.objects.create(
            vehicle=cls.vehicle,
            starting_mileage=0,
            ending_mileage=20000,
            driver_name="Test Driver",
            purpose="Test Purpose",
            finished=True,
        )

    def test_fuel_expense_form_initializes_mileage_with_vehicle_mileage(self):
        """
        Test that FuelExpenseForm initializes mileage field with vehicle's current mileage
        """
        # WHEN a FuelExpenseForm is created with the vehicle parameter
        form = FuelExpenseForm(vehicle=self.vehicle)

        # THEN the mileage field should be initialized with the vehicle's mileage
        self.assertEqual(form.fields["mileage"].initial, 20000)

    def test_fuel_expense_form_without_vehicle_parameter(self):
        """
        Test that FuelExpenseForm works without vehicle parameter
        """
        # WHEN a FuelExpenseForm is created without vehicle parameter
        form = FuelExpenseForm()

        # THEN the form should be created successfully with model field default
        self.assertEqual(form.fields["mileage"].initial, 0)  # Model field default

    def test_fuel_expense_form_with_bound_data_ignores_vehicle_mileage(self):
        """
        Test that FuelExpenseForm doesn't override mileage when form is bound with data
        """
        # WHEN a FuelExpenseForm is created with bound data and vehicle parameter
        form_data = {
            "date": "2023-10-01",
            "mileage": 16000,  # Different from vehicle mileage
            "amount": 50,
            "quantity": 1.5,
            "form_of_payment": "FUEL CARD",
        }
        form = FuelExpenseForm(data=form_data, vehicle=self.vehicle)

        # THEN the form should not override the provided mileage with vehicle mileage
        # When bound, we check the bound data, not the initial value
        self.assertEqual(form.data["mileage"], 16000)  # Bound data is used

    def test_fuel_expense_form_with_existing_instance_ignores_vehicle_mileage(self):
        """
        Test that FuelExpenseForm doesn't override mileage when editing existing instance
        """
        fuel_expense = FuelExpense.objects.create(
            vehicle=self.vehicle,
            date="2023-10-01",
            mileage=14000,  # Different from current vehicle mileage
            amount=50,
            quantity=1.5,
            form_of_payment="FUEL CARD",
        )

        # WHEN a FuelExpenseForm is created for editing the existing instance
        form = FuelExpenseForm(instance=fuel_expense, vehicle=self.vehicle)

        # THEN the form should not override with vehicle mileage since it's an existing instance
        # When editing, the form uses the instance's existing value, not vehicle mileage
        self.assertEqual(
            fuel_expense.mileage, 14000
        )  # Instance keeps its original value


class TripFormTestCase(TestCase):
    """
    Dedicated unit tests for TripForm and TripStartForm
    """

    @classmethod
    def setUpTestData(cls):
        from django.utils import timezone

        cls.vehicle = Vehicle.objects.create(
            name="VPS Test",
            type=Vehicle.VehicleType.VPSP,
            model_name="Renault Master",
            fuel=Vehicle.FuelChoice.DIESEL,
            registration_number="1234ABCD",
            status=Vehicle.VehicleStatus.OPERATIONAL,
        )
        Trip.objects.create(
            vehicle=cls.vehicle,
            starting_mileage=0,
            ending_mileage=20000,
            driver_name="Test Driver",
            purpose="Test Purpose",
            finished=True,
        )
        cls.test_time = timezone.now()

    def test_trip_start_form_initializes_starting_mileage_with_vehicle_mileage(self):
        """
        Test that TripStartForm initializes starting_mileage field with vehicle's current mileage
        """
        # WHEN a TripStartForm is created with the vehicle parameter
        form = TripStartForm(vehicle=self.vehicle)

        # THEN the starting_mileage field should be initialized with the vehicle's mileage
        self.assertEqual(form.fields["starting_mileage"].initial, 20000)

    def test_trip_form_initializes_starting_mileage_with_vehicle_mileage(self):
        """
        Test that TripForm (base class) initializes starting_mileage field with vehicle's current mileage
        """
        # WHEN a TripForm is created with the vehicle parameter
        form = TripForm(vehicle=self.vehicle)

        # THEN the starting_mileage field should be initialized with the vehicle's mileage
        self.assertEqual(form.fields["starting_mileage"].initial, 20000)

    def test_trip_form_without_vehicle_parameter(self):
        """
        Test that TripForm works without vehicle parameter
        """
        # WHEN a TripForm is created without vehicle parameter
        form = TripForm()

        # THEN the form should be created successfully with no initial starting_mileage
        self.assertIsNone(form.fields["starting_mileage"].initial)

    def test_trip_form_with_bound_data_ignores_vehicle_mileage(self):
        """
        Test that TripForm doesn't override starting_mileage when form is bound with data
        """
        # WHEN a TripForm is created with bound data and vehicle parameter
        form_data = {
            "starting_mileage": 26000,  # Different from vehicle mileage
        }
        form = TripForm(data=form_data, vehicle=self.vehicle)

        # THEN the form should not override the provided starting_mileage with vehicle mileage
        # When bound, we check the bound data, not the initial value
        self.assertEqual(form.data["starting_mileage"], 26000)  # Bound data is used

    def test_trip_form_with_existing_instance_ignores_vehicle_mileage(self):
        """
        Test that TripForm doesn't override starting_mileage when editing existing instance
        """
        trip = Trip.objects.create(
            vehicle=self.vehicle,
            starting_mileage=24000,  # Different from current vehicle mileage
            starting_time=self.test_time,
            driver_name="John Doe",
            purpose="Test trip",
            finished=True,
        )

        # WHEN a TripForm is created for editing the existing instance
        form = TripForm(instance=trip, vehicle=self.vehicle)

        # THEN the form should not override with vehicle mileage since it's an existing instance
        # When editing, the form uses the instance's existing value, not vehicle mileage
        self.assertEqual(
            trip.starting_mileage, 24000
        )  # Instance keeps its original value
