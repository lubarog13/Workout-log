from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField()
    date_birth = models.DateField()
    sex = models.CharField(max_length=1, choices={('М', 'М'), ('Ж', 'Ж')})
    is_coach = models.BooleanField(blank=True, null=True)
    club = models.ManyToManyField("Club", through="SignUp")
    REQUIRED_FIELDS = ['first_name', 'last_name',  'date_birth', 'sex', 'is_coach']


class Message(models.Model):
    heding = models.CharField(max_length=100)
    message = models.TextField(max_length=3000, blank=True, null=True)
    send_time = models.DateTimeField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')


class Coach(models.Model):
    post = models.TextField(max_length=75)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Building(models.Model):
    city = models.CharField(max_length=45)
    address = models.CharField(max_length=100)
    number = models.PositiveIntegerField()
    liter = models.CharField(max_length=1, blank=True, null=True)


class Hall(models.Model):
    name = models.TextField()
    number = models.PositiveIntegerField(blank=True, null=True)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    occupancy = models.PositiveIntegerField()


class Club(models.Model):
    identifier = models.CharField(max_length=45, unique=True)
    name = models.TextField()
    group = models.TextField()
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)


class SignUp(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


class Workout(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    type = models.TextField(choices={('кардио', 'кардио'),
                                     ('силовая', 'силовая'),
                                     ('на технику', 'на технику'),
                                     ('общая', 'общая'),
                                     ('другое', 'другое')})
    other_type = models.TextField(blank=True, null=True)
    is_carried_out = models.BooleanField(default=False)
    coach_replace = models.ForeignKey(Coach, on_delete=models.CASCADE, blank=True, null=True)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, through="Presence")


class Presence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    is_attend = models.BooleanField(default=False)
    reason = models.TextField(blank=True, null=True)
    delay = models.BooleanField(default=False)
    early_ret = models.BooleanField(default=False)