from django.test import TestCase

from main.models import Vehicle


class FuelExpenseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.vehicle = Vehicle.objects.create(
            name="VPS Test",
            type=Vehicle.VehicleType.VPSP,
            model_name="Renault Master",
            fuel=Vehicle.FuelChoice.DIESEL,
            registration_number="1234ABCD",
            status=Vehicle.VehicleStatus.OPERATIONAL,
            mileage=10,
        )

    def test_create_fuel_expense_valid(self):
        """
        Test the creation of a fuel expense with valid data
        """

        # GIVEN a vehicle with no fuel expenses

        # WHEN a fuel expense is created with valid data
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/fuel-expense",
            {
                "date": "2023-10-01",
                "mileage": "100",
                "amount": "50",
                "quantity": "1.5",
                "form_of_payment": "FUEL CARD",
            },
        )

        # THEN the fuel expense should be created and the user should be redirected to the vehicle details page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")
        self.assertEqual(self.vehicle.fuelexpense_set.count(), 1)
        self.assertEqual(self.vehicle.fuelexpense_set.first().mileage, 100)
        self.assertEqual(self.vehicle.fuelexpense_set.first().amount, 50)
        self.assertEqual(self.vehicle.fuelexpense_set.first().quantity, 1.5)
        self.assertEqual(self.vehicle.fuelexpense_set.first().vehicle, self.vehicle)
        self.assertEqual(
            self.vehicle.fuelexpense_set.first().date.isoformat(), "2023-10-01"
        )
        self.assertEqual(
            self.vehicle.fuelexpense_set.first().form_of_payment, "FUEL CARD"
        )
