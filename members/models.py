from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


class Faculty(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class FieldOfStudy(models.Model):
    name = models.CharField(max_length=250)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=250)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profile(models.Model):
    MODES = [
        ('f', 'stacjonarne'),
        ('p', 'niestacjonarne')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.DO_NOTHING)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.DO_NOTHING)
    specialization = models.ForeignKey(Specialization, on_delete=models.DO_NOTHING)
    index_number = models.CharField(max_length=6, blank=True, unique=True, validators=RegexValidator(regex='\d{6}', message='Incorrect index number'))
    mode = models.CharField(blank=True, choices=MODES)
    address = models.CharField(max_lenght=255, blank=True, validators=RegexValidator(regex='^(Os\.)|(Ul\.) ([A-z]| )+ (\d)*/?(\d)*$', message='Incorrect address or wrong format'))
    zip_code = models.CharField(max_lenght=6, blank=True, validators=RegexValidator(regex='^\d{2}-\d{3}$', message='Incorrect zip_code'))
    city = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=255, blank=True)
    municipality = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=True)


    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
