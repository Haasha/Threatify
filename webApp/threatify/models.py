from django.db import models
from timezone_field import TimeZoneField
from django_countries.fields import CountryField
from django.core import validators

Types = (('1', 'Live'), ('2', 'Recorded'))


# Create your models here.
class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Email = models.EmailField(max_length=254)
    Password = models.CharField(max_length=100)
    Phone = models.CharField(max_length=20, blank=True)
    SSN = models.CharField(max_length=50, blank=True)
    AddressLine1 = models.CharField(max_length=50, blank=True)
    AddressLine2 = models.CharField(max_length=50, blank=True)
    City = models.CharField(max_length=50, blank=True)
    Country = CountryField(blank_label='(select country)', blank=True)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0.0)
    Latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, default=0.0)
    TimeZone = TimeZoneField(choices_display='WITH_GMT_OFFSET', blank=True)

    def __str__(self):
        return str(self.UserID) + '_' + self.Name


class Feed(models.Model):
    CameraID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    CameraLocation = models.CharField(max_length=50)
    Url = models.URLField(validators=[validators.URLValidator])
    Username = models.CharField(max_length=100, blank=True)
    Password = models.CharField(max_length=100, blank=True)
    MotionDetection = models.BooleanField(default=False)
    MotionAlert = models.BooleanField(default=False)
    MotionSensitivity = models.IntegerField(
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)], default=0)

    CrimeDetection = models.BooleanField(default=False)
    CrimeAlert = models.BooleanField(default=False)
    CrimeSensitivity = models.IntegerField(
        validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)], default=0)

    def __str__(self):
        return str(self.UserID) + '_' + str(self.CameraID)


class Threat(models.Model):
    ThreatID = models.IntegerField(primary_key=True)
    Threat = models.CharField(max_length=100)
    ReportTo = models.CharField(max_length=100)

    def __str__(self):
        return str(self.Threat)


class ThreatLog(models.Model):
    ThreatID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    CameraID = models.ForeignKey(Feed, on_delete=models.CASCADE)
    File = models.FileField()
    TimeStamp = models.DateTimeField()
    Category = models.ForeignKey(Threat, on_delete=models.CASCADE)
    Duration = models.DurationField()

    Confidence = models.FloatField()
    Type = models.CharField(max_length=8, choices=Types, default=Types[0])

    def __str__(self):
        return str(self.UserID) + '_' + str(self.ThreatID)
