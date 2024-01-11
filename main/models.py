from django.db import models
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):
    class Meta:
        verbose_name = _("véhicule")

    class VehicleType(models.TextChoices):
        VTP = "VTP", _("VTP - Véhicule de Transport de Personnel")

    class VehicleStatus(models.TextChoices):
        OPERATIONAL = 'OPERATIONAL', _("Opérationnel")
        IN_REPAIR = 'IN_REPAIR', _("En réparation")
        OUT_OF_ORDER = 'OUT_OF_ORDER', _("En panne")

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
    registration_number = models.CharField(_("numéro d'immatriculation"), max_length=255)
    parking_location = models.ForeignKey("Location", verbose_name=_("emplacement"), on_delete=models.CASCADE, blank=True)
    status = models.CharField(_("statut"), choices=VehicleStatus, default=VehicleStatus.OPERATIONAL, max_length=255)

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
        }
    }

    class DefectStatus(models.TextChoices):
        OPEN = 'OPEN', _("ouvert")
        SOLVED = 'SOLVED', _("résolu")
        CANCELLED = 'CANCELLED', _("annulé")

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    type = models.CharField(_("type d'anomalie"), max_length=255, choices=DEFECT_TYPE)
    status = models.CharField(_("statut"), max_length=255, choices=DefectStatus)
    creation_date = models.DateField(_("date de création"), auto_now_add=True)
    solution_date = models.DateField(_("date de résolution"), null=True, blank=True)
    comment = models.TextField(_("Notes"), blank=True)


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


