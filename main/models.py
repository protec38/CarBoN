import datetime
import uuid

from django.utils import timezone
from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core import mail
from django.template import Context, loader


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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("identifiant"), max_length=255)
    type = models.CharField(_("type de véhicule"), max_length=255, choices=VehicleType)
    model_name = models.CharField(_("Marque et modèle"), max_length=255)
    fuel = models.CharField(_("carburant"), max_length=255, choices=FuelChoice)
    registration_number = models.CharField(
        _("numéro d'immatriculation"), max_length=255
    )
    parking_location = models.ForeignKey(
        "Location",
        verbose_name=_("emplacement"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    status = models.CharField(
        _("statut"),
        choices=VehicleStatus,
        default=VehicleStatus.OPERATIONAL,
        max_length=255,
    )
    mileage = models.PositiveIntegerField(_("kilométrage"), default=0)
    inventory = models.URLField(_("inventaire"), null=True, blank=True)

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
        OPEN = "OPEN", _("Ouvert")
        CONFIRMED = "CONFIRMED", _("Confirmé")
        SOLVED = "SOLVED", _("Résolu")
        CANCELLED = "CANCELLED", _("Annulé")

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

    def save(self, *args, **kwargs):
        # Send an email notification when a defect is created
        if not self.pk:  # Only send email on creation
            recipient_list = Setting.manager.read("defect_notification_email").split(",")
            from_email = Setting.manager.read("from_email")
            
            from main import utils # Avoiding circular import issues
            email_backend = utils.get_email_backend()

            context = {
                "vehicle": self.vehicle.name,
                "type": self.get_type_display(),
                "comment": self.comment,
                "reporter": self.reporter_name
            }

            plaintext_content = loader.render_to_string("main/email/defect.txt", context)
            html_content = loader.render_to_string("main/email/defect.html", context)

            mail.send_mail(
                subject=_("Anomalie signalée pour le véhicule {name}").format(name= self.vehicle.name),
                message=plaintext_content,
                from_email=from_email,
                recipient_list=[email.strip() for email in recipient_list if email.strip()],
                html_message=html_content,
                connection=email_backend,
            )
            
        super().save(*args, **kwargs)


class Location(models.Model):
    class Meta:
        verbose_name = _("Parking")

    name = models.CharField(_("nom"), max_length=255)
    address = models.CharField(_("adresse"), max_length=255)
    zip_code = models.CharField(_("code postal"), max_length=255)
    city = models.CharField(_("ville"), max_length=255)
    comment = models.TextField(_("notes"), blank=True)

    @property
    def complete_address(self):
        return f"{ self.address } - {self.zip_code } { self.city }"

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

    @admin.display(description="Distance parcourue")
    def distance(self):
        if self.finished and None not in (self.starting_mileage, self.ending_mileage):
            return self.ending_mileage - self.starting_mileage

        return None

    @admin.display(description="Durée")
    def duration(self):
        if self.finished and None not in (self.starting_time, self.ending_time):
            return self.ending_time - self.starting_time

        return None

    def clean(self):
        validation_errors = dict()

        if self.starting_mileage < self.vehicle.mileage:
            validation_errors["starting_mileage"] = ValidationError(
                _(
                    "Le kilométrage de départ ne peut pas être inférieur au kilométrage du véhicule !"
                ),
                code="invalid_mileage",
            )

        if self.ending_mileage and self.starting_mileage > self.ending_mileage:
            validation_errors["ending_mileage"] = ValidationError(
                _(
                    "Le kilométrage de fin ne peut pas être inférieur au kilométrage de départ !"
                ),
                code="invalid_mileage",
            )

        if self.ending_time and self.starting_time > self.ending_time:
            validation_errors["ending_time"] = ValidationError(
                _("L'arrivée doit avoir lieu après le départ !"), code="invalid_time"
            )

        if len(validation_errors) > 0:
            raise ValidationError(validation_errors)


class FuelExpense(models.Model):
    class Meta:
        verbose_name = _("Dépense de carburant")
        verbose_name_plural = _("Dépenses de carburant")

    vehicle = models.ForeignKey(
        Vehicle, verbose_name=_("véhicule"), on_delete=models.CASCADE
    )
    date = models.DateField(_("date"), default=datetime.date.today)
    mileage = models.IntegerField(_("kilométrage"), default=0)
    amount = models.DecimalField(_("montant / €"), decimal_places=2, max_digits=5)
    quantity = models.DecimalField(_("quantité / L"), decimal_places=2, max_digits=5)

class SettingManager(models.Manager):
    def read(self, key, default=""):
        try:
            value = super().get(key=key).value
        except Setting.DoesNotExist:
            value = default

        return value
    
    def read_boolean(self, key, default=False):
        value = self.read(key)
        if value == "":
            return default
        
        return value.lower() in ("true", "1", "yes")
        

class Setting(models.Model):
    class Meta:
        verbose_name = _("paramètre")
        verbose_name_plural = _("paramètres")
        
    key = models.CharField(_("clé"), max_length=255, unique=True)
    value = models.CharField(_("valeur"), max_length=255, blank=True, default="")
    manager = SettingManager()

    def __str__(self):
        return f"{self.key}: {self.value}"