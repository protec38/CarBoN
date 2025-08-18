from django.test import TestCase

from main.models import Vehicle


class DefectsTestCase(TestCase):
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

    def test_create_defect_valid(self):
        """
        Test the creation of a defect with valid data
        """

        # GIVEN a vehicle with no defects

        # WHEN a defect is created with valid data
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/defect",
            {
                "type": "engine",
                "comment": "Engine is making a weird noise",
                "reporter_name": "John Doe",
            },
        )

        # THEN the defect should be created and the user should be redirected to the vehicle details page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")
        self.assertEqual(self.vehicle.defect_set.count(), 1)
        self.assertEqual(self.vehicle.defect_set.first().type, "engine")
        self.assertEqual(
            self.vehicle.defect_set.first().comment, "Engine is making a weird noise"
        )
        self.assertEqual(self.vehicle.defect_set.first().reporter_name, "John Doe")

    def test_create_defect_invalid_missing_type(self):
        """
        Test the creation of a defect with missing type
        """
        # GIVEN a vehicle with no defects

        # WHEN a defect is created with missing type
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/defect",
            {
                "comment": "Engine is making a weird noise",
                "reporter_name": "John Doe",
            },
        )

        # THEN the defect should not be created and the user should be redirected to the vehicle details page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")
        self.assertEqual(self.vehicle.defect_set.count(), 0)
