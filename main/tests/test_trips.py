from django.test import TestCase
from django.utils import timezone
from django.core import mail

from main.models import Vehicle, Trip, Setting


class TripTestCase(TestCase):
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
            starting_time=timezone.now(),
            ending_mileage=10,
            ending_time=timezone.now(),
            driver_name="John Doe",
            purpose="DPS",
            finished=True,
        ).save()

        cls.vehicle.save()

        cls.test_time = timezone.make_aware(
            timezone.datetime.fromisoformat("2021-01-01T00:00")
        )

        cls.email_recipients = ["vehicules1@mail.com", "vehicules2@mail.com"]
        Setting.manager.create(
            key="defect_notification_email", value=", ".join(cls.email_recipients)
        )

    def test_start_trip_valid(self):
        """
        Test the creation of a trip with valid data
        """
        # GIVEN a vehicle with a mileage of 10

        # WHEN a trip is started with a starting mileage of 15 and valid data
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/trip-start",
            {
                "starting_mileage": 15,
                "starting_time": self.test_time.isoformat(),
                "driver_name": "John Doe",
                "purpose": "DPS",
            },
        )

        # THEN the trip should be started and the user should be redirected to the vehicle details page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")

        vehicle = Vehicle.objects.get(pk=self.vehicle.id)
        self.assertEqual(vehicle.trip_set.count(), 2)
        self.assertEqual(vehicle.trip_set.last().finished, False)
        self.assertEqual(vehicle.trip_set.last().starting_mileage, 15)
        self.assertEqual(vehicle.trip_set.last().starting_time, self.test_time)
        self.assertEqual(vehicle.trip_set.last().driver_name, "John Doe")
        self.assertEqual(vehicle.trip_set.last().purpose, "DPS")

        self.assertEqual(vehicle.trip_set.last().distance(), None)
        self.assertEqual(vehicle.trip_set.last().duration(), None)

        # AND a notification should not be sent yet, even if the starting mileage is higher than the vehicle's
        self.assertEqual(len(mail.outbox), 0)

    def test_start_trip_mileage_invalid(self):
        """
        Test the creation of a trip with invalid mileage (lower than the current mileage)
        """
        # GIVEN a vehicle with a mileage of 10

        # WHEN a trip is started with a starting mileage of 5
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/trip-start",
            {
                "starting_mileage": 0,
                "starting_time": "2021-01-01T00:00",
                "driver_name": "John Doe",
                "purpose": "DPS",
            },
        )

        # THEN the trip should not be started and the user should be redirected to the vehicle details page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")

        vehicle = Vehicle.objects.get(pk=self.vehicle.id)
        self.assertEqual(vehicle.trip_set.count(), 1)

    def test_end_trip_valid(self):
        """
        Test the end of a trip with valid data (no modification of the starting data)
        """

        # GIVEN a started trip
        self.test_start_trip_valid()

        # WHEN the trip is ended with valid data (no modification of the starting data)
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/trip-end",
            {
                "starting_mileage": 15,
                "starting_time": self.test_time.isoformat(),
                "driver_name": "John Doe",
                "purpose": "DPS",
                "ending_mileage": 20,
                "ending_time": (
                    self.test_time + timezone.timedelta(hours=1)
                ).isoformat(),
            },
        )

        # THEN the trip should be ended and the user should be redirected to the vehicle details page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")

        vehicle = Vehicle.objects.get(pk=self.vehicle.id)
        self.assertEqual(vehicle.trip_set.count(), 2)
        self.assertEqual(vehicle.trip_set.last().finished, True)
        self.assertEqual(vehicle.mileage, 20)
        self.assertEqual(vehicle.trip_set.last().distance(), 5)
        self.assertEqual(
            vehicle.trip_set.last().duration(), timezone.timedelta(hours=1)
        )

        # AND a notification should be sent as the starting mileage is higher than the mileage of the vehicle
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(sorted(mail.outbox[0].to), sorted(self.email_recipients))
        self.assertIn(
            "Trajet manquant pour le véhicule VPS Test", mail.outbox[0].subject
        )

    def test_end_trip_modified_starting_mileage_without_flag(self):
        """
        Test the end of a trip with valid data and modification of the starting mileage, without the `update_initial` flag. The starting mileage should not be updated.
        """
        # GIVEN a started trip
        self.test_start_trip_valid()

        # WHEN the trip is ended without the `update_initial` flag and starting mileage is modified
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/trip-end",
            {
                "starting_mileage": 16,
                "starting_time": self.test_time.isoformat(),
                "driver_name": "John Doe",
                "purpose": "DPS",
                "ending_mileage": 20,
                "ending_time": (
                    self.test_time + timezone.timedelta(hours=1)
                ).isoformat(),
            },
        )

        # THEN the trip should be ended and the starting mileage should not be updated (it should remain at 15). The user should be redirected to the vehicle details page.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")

        vehicle = Vehicle.objects.get(pk=self.vehicle.id)
        self.assertEqual(vehicle.trip_set.count(), 2)
        self.assertEqual(vehicle.trip_set.last().finished, True)
        self.assertEqual(vehicle.trip_set.last().starting_mileage, 15)

    def test_end_trip_modified_starting_mileage_with_flag(self):
        """ "
        Test the end of a trip with valid data and modification of the starting mileage, with the `update_initial` flag. The starting mileage should be updated.
        """
        # GIVEN a started trip
        self.test_start_trip_valid()

        # WHEN the trip is ended with the `update_initial` flag and starting mileage is modified
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/trip-end",
            {
                "starting_mileage": 16,
                "starting_time": self.test_time.isoformat(),
                "driver_name": "John Doe",
                "purpose": "DPS",
                "ending_mileage": 20,
                "ending_time": (
                    self.test_time + timezone.timedelta(hours=1)
                ).isoformat(),
                "update_initial": True,
            },
        )

        # THEN the trip should be ended and the starting mileage should be updated. The user should be redirected to the vehicle details page.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")

        vehicle = Vehicle.objects.get(pk=self.vehicle.id)
        self.assertEqual(vehicle.trip_set.count(), 2)
        self.assertEqual(vehicle.trip_set.last().finished, True)
        self.assertEqual(vehicle.trip_set.last().starting_mileage, 16)

    def test_end_trip_time_invalid(self):
        """
        Test the end of a trip with invalid data (ending time before starting time)
        """

        # GIVEN a started trip
        self.test_start_trip_valid()

        # WHEN the trip is ended with invalid data (ending time before starting time)
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/trip-end",
            {
                "starting_mileage": 15,
                "starting_time": self.test_time.isoformat(),
                "driver_name": "John Doe",
                "purpose": "DPS",
                "ending_mileage": 20,
                "ending_time": (
                    self.test_time - timezone.timedelta(hours=1)
                ).isoformat(),
            },
        )

        # THEN the trip should not be ended and the user should be redirected to the vehicle details page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")

        vehicle = Vehicle.objects.get(pk=self.vehicle.id)
        self.assertEqual(vehicle.trip_set.count(), 2)
        self.assertEqual(vehicle.trip_set.last().finished, False)
        self.assertEqual(vehicle.mileage, 10)

    def test_end_trip_mileage_invalid(self):
        """
        Test the end of a trip with invalid data (ending mileage lower than starting mileage)
        """

        # GIVEN a started trip
        self.test_start_trip_valid()

        # WHEN the trip is ended with invalid data (ending mileage lower than starting mileage)
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/trip-end",
            {
                "starting_mileage": 15,
                "starting_time": self.test_time.isoformat(),
                "driver_name": "John Doe",
                "purpose": "DPS",
                "ending_mileage": 10,
                "ending_time": (
                    self.test_time + timezone.timedelta(hours=1)
                ).isoformat(),
            },
        )

        # THEN the trip should not be ended and the data should not be saved. The user should be redirected to the vehicle details page.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")

        vehicle = Vehicle.objects.get(pk=self.vehicle.id)
        self.assertEqual(vehicle.trip_set.count(), 2)
        self.assertEqual(vehicle.trip_set.last().finished, False)
        self.assertEqual(vehicle.mileage, 10)

    def test_abort_trip(self):
        """
        Test the abortion of a trip
        """

        # GIVEN a started trip
        self.test_start_trip_valid()

        # WHEN the trip is aborted
        response = self.client.post(
            f"/vehicles/{self.vehicle.id}/trip-abortion",
            {},
        )

        # THEN the trip is marked as finished and the ending data is not set. The user should be redirected to the vehicle details page.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/vehicles/{self.vehicle.id}")

        vehicle = Vehicle.objects.get(pk=self.vehicle.id)
        self.assertEqual(vehicle.trip_set.count(), 2)
        self.assertEqual(vehicle.trip_set.last().finished, True)
        self.assertEqual(vehicle.trip_set.last().ending_mileage, None)
        self.assertEqual(vehicle.trip_set.last().ending_time, None)

        # AND a notification should be sent as the trip was aborted
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(sorted(mail.outbox[0].to), sorted(self.email_recipients))
        self.assertIn(
            "Trajet abandonné pour le véhicule VPS Test", mail.outbox[1].subject
        )

    def test_check_disabled_in_admin(self):
        """
        Test that the mileage and time fields are not check for inconsistencies
        when the trip is created in the admin interface.
        """
        # GIVEN a vehicle with a mileage of 10 with a trip

        trip = Trip.objects.create(
            vehicle=self.vehicle,
            starting_mileage=self.vehicle.mileage + 10,
            starting_time=self.test_time.isoformat(),
            driver_name="John Doe",
            purpose="DPS",
        )

        # WHEN the trip is changed with a starting mileage lower than the mileage of the vehicle in the admin interface
        response = self.client.post(
            f"/admin/main/trip/{trip.id}/change/",
            {
                "vehicle": self.vehicle.id,
                "starting_mileage": self.vehicle.mileage - 10,
                "starting_time": "2021-01-01T00:00",
                "driver_name": "John Doe",
                "purpose": "DPS",
            },
        )
        # THEN the trip should be created without any validation errors
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.vehicle.trip_set.count(), 2)
