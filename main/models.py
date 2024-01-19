from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Vehicle(models.Model):
    class Meta:
        verbose_name = _("véhicule")

    class VehicleType(models.TextChoices):
        VTP = "VTP", _("VTP - Véhicule de Transport de Personnel")
        VL = "VL", _("VL - Véhicule Léger")
        VPSP = "VPSP", _("VPSP - Véhicule de Premiers Secours à Personnes")
        VTU = "VTU", _("VTU - Véhicule Tout Usage")
        VLTT = "VLTT", _("VLTT - Véhicule Léger Tout Terrain")
        OTHER = "OTHER", _("Autre")

    class VehicleStatus(models.TextChoices):
        OPERATIONAL = "OPERATIONAL", _("Opérationnel")
        IN_REPAIR = "IN_REPAIR", _("En réparation")
        OUT_OF_ORDER = "OUT_OF_ORDER", _("En panne")

    class FuelChoice(models.TextChoices):
        DIESEL = "DIESEL", _("Gasoil")
        UNLEADED_95_10 = "UNLEADED_95_10", _("SP 95-E10")
        UNLEADED_98 = "UNLEADED_98", _("SP 98")
        ETHANOL = "ETHANOL", _("E85")
        ELECTRIC = "ELECTRIC", _("Électrique")

    name = models.CharField(_("identifiant"), max_length=255)
    type = models.CharField(_("type de véhicule"), max_length=255, choices=VehicleType)
    model_name = models.CharField(_("Marque et modèle"), max_length=255)
    carburant = models.CharField(_("carburant"), max_length=255, choices=FuelChoice)
    registration_number = models.CharField(
        _("numéro d'immatriculation"), max_length=255
    )
    parking_location = models.ForeignKey(
        "Location", verbose_name=_("emplacement"), on_delete=models.CASCADE, blank=True
    )
    status = models.CharField(
        _("statut"),
        choices=VehicleStatus,
        default=VehicleStatus.OPERATIONAL,
        max_length=255,
    )
    mileage = models.PositiveIntegerField(_("kilométrage"), default=0)

    def __str__(self):
        return self.name


class Defect(models.Model):
    class Meta:
        verbose_name = _("anomalie")

    DEFECT_TYPE = {
        _("mécanique"): {
            "engine": _("moteur"),
        },
        _("éclairage"): {
            "bulb": _("ampoule"),
        },
    }

    class DefectStatus(models.TextChoices):
        OPEN = "OPEN", _("ouvert")
        SOLVED = "SOLVED", _("résolu")
        CANCELLED = "CANCELLED", _("annulé")

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    type = models.CharField(_("type d'anomalie"), max_length=255, choices=DEFECT_TYPE)
    status = models.CharField(
        _("statut"), max_length=255, choices=DefectStatus, default=DefectStatus.OPEN
    )
    creation_date = models.DateField(_("date de création"), auto_now_add=True)
    solution_date = models.DateField(
        _("date de résolution"), null=True, blank=True, editable=False
    )
    comment = models.TextField(_("Notes"), blank=True)
    reporter_name = models.CharField(
        _("Nom"),
        max_length=255,
        help_text="Nom de la personne rapportant l'erreur",
    )


class Location(models.Model):
    class Meta:
        verbose_name = _("adresse")

    name = models.CharField(_("nom"), max_length=255)
    address = models.CharField(_("adresse"), max_length=255)
    zip_code = models.CharField(_("code postal"), max_length=255)
    city = models.CharField(_("ville"), max_length=255)
    comment = models.TextField(_("notes"), blank=True)

    def __str__(self):
        return self.name


class Trip(models.Model):
    class Meta:
        verbose_name = _("trajet")

    vehicle = models.ForeignKey(
        Vehicle, verbose_name=_("véhicule"), on_delete=models.CASCADE
    )
    starting_mileage = models.PositiveIntegerField(_("kilométrage de départ"))
    ending_mileage = models.PositiveIntegerField(
        _("kilométrage d'arrivée"), blank=True, null=True
    )
    starting_time = models.DateTimeField(_("heure de départ"), default=timezone.now)
    ending_time = models.DateTimeField(_("heure d'arrivée"), blank=True, null=True)
    driver_name = models.CharField(_("nom du conducteur"), max_length=255)
    purpose = models.CharField(_("motif du déplacement"), max_length=255)
    finished = models.BooleanField(_("terminé"), editable=False, default=False)

    def clean(self):
        validation_errors = dict()

        if self.starting_mileage < self.vehicle.mileage:
            validation_errors["starting_mileage"] = ValidationError(
                _(
                    "Le kilométrage de départ ne peut pas être inférieur au kilométrage du véhicule !"
                )
            )

        if self.ending_mileage and self.starting_mileage > self.ending_mileage:
            validation_errors["ending_mileage"] = ValidationError(
                _(
                    "Le kilométrage de fin ne peut pas être inférieur au kilométrage de départ !"
                ),
                code="invalid",
            )

        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)
