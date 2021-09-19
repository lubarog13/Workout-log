from django.db import models
from django.contrib.auth.models import AbstractUser

# Пользователь
class User(AbstractUser):
    second_name = models.TextField(blank=True, null=True)                  # Отчество
    email = models.EmailField()                                            # email
    date_birth = models.DateField()                                        # Дата рождения
    sex = models.CharField(max_length=1, choices={('М', 'М'), ('Ж', 'Ж')}) # Пол
    is_coach = models.BooleanField(blank=True, null=True)                  # Это_тренер
    club = models.ManyToManyField("Club", through="SignUp")                # Секции
    REQUIRED_FIELDS = ['first_name', 'last_name', 'second_name', 'email', 'date_birth', 'sex', 'is_coach']


# Сообщение
class Message(models.Model):
    heding = models.CharField(max_length=100)                                               # Заголовок
    message = models.TextField(max_length=3000, blank=True, null=True)                      # Текст сообщения
    send_time = models.DateTimeField()                                                      # Время отправления
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')       # Отправитель
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient') # Получатель


# Тренер
class Coach(models.Model):
    post = models.TextField(max_length=75)                   # Должность
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Пользователь


# Здание
class Building(models.Model):
    city = models.CharField(max_length=45)                        # Город
    address = models.CharField(max_length=100)                    # Адрес
    number = models.PositiveIntegerField()                        # Номер
    liter = models.CharField(max_length=1, blank=True, null=True) # Литера


# Зал
class Hall(models.Model):
    name = models.TextField()                                        # Название
    number = models.PositiveIntegerField(blank=True, null=True)      # Номер
    building = models.ForeignKey(Building, on_delete=models.CASCADE) # Здание
    occupancy = models.PositiveIntegerField()                        # Вместимоть


# Секция
class Club(models.Model):
    identifier = models.CharField(max_length=45, unique=True)        # Идентификатор
    name = models.TextField()                                        # Название
    group = models.TextField()                                       # Группа
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)       # Тренер
    building = models.ForeignKey(Building, on_delete=models.CASCADE) # Здание

# Запись
class SignUp(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE) # Секция
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Пользователь
    start_date = models.DateField()                          # Дата начала
    end_date = models.DateField()                            # Дата конца


# Тренировка
class Workout(models.Model):
    start_time = models.DateTimeField()                                                       # Время начала
    end_time = models.DateTimeField()                                                         # Время окончания
    type = models.TextField(choices={('кардио', 'кардио'),
                                     ('силовая', 'силовая'),
                                     ('на технику', 'на технику'),
                                     ('общая', 'общая'),
                                     ('другое', 'другое')})                                   # Тип
    other_type = models.TextField(blank=True, null=True)                                      # Другой тип
    is_carried_out = models.BooleanField(default=False)                                       # Была проведена
    coach_replace = models.ForeignKey(Coach, on_delete=models.CASCADE, blank=True, null=True) # Тренер на замену
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)                                  # Зал
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True)           # Секция
    user = models.ManyToManyField(User, through="Presence")                                   # Пользователь


# Присутствие
class Presence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)       # Пользователь
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE) # Тренировка
    is_attend = models.BooleanField(default=False)                 # Присутствие
    reason = models.TextField(blank=True, null=True)               # Причина
    delay = models.BooleanField(default=False)                     # Опозание
    early_ret = models.BooleanField(default=False)                 # Ранний уход