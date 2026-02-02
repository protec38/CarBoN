from django.test import TestCase
from django.core import mail

from main.models import Vehicle, Setting


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
                "comment": "Engine is making a weird noise",
                "reporter_name": "John Doe",
            },
        )

        # THEN the defect should be created and the user should be redirected to the vehicle details page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")
        self.assertEqual(self.vehicle.defect_set.count(), 1)
        self.assertEqual(
            self.vehicle.defect_set.first().comment, "Engine is making a weird noise"
        )
        self.assertEqual(self.vehicle.defect_set.first().reporter_name, "John Doe")

    def test_email_notification_on_defect_creation(self):
        """
        Test that an email notification is sent when a defect is created
        """
        # GIVEN a vehicle with no defects
        email_recipients = ["vehicules1@mail.com", "vehicules2@mail.com"]
        Setting.manager.create(
            key="defect_notification_email",
            value=", ".join(email_recipients))
        
        # WHEN a defect is created
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/defect",
            {
                "comment": "Engine is making a weird noise",
                "reporter_name": "Jane Doe",
            },
        )
        
        # THEN an email should be sent to the admin
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(sorted(mail.outbox[0].to), sorted(email_recipients))
        self.assertIn("Anomalie signalée pour le véhicule VPS Test", mail.outbox[0].subject)
        self.assertIn("Engine is making a weird noise", mail.outbox[0].body)