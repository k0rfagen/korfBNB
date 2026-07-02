from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class Role(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}'


class BNBUser(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, default=1)


class Listing(models.Model):
    owner = models.ForeignKey(BNBUser, on_delete=models.CASCADE)
    date_published = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, default='none')
    description = models.TextField(default='nothing yet')
    price_per_night = models.IntegerField(
        validators=[
            MaxValueValidator(10000),
            MinValueValidator(3),
        ],
        default=15
    )
    location = models.CharField(max_length=50, default='Moscow')
    rooms_count = models.IntegerField(
        validators=[
            MaxValueValidator(20),
            MinValueValidator(1),
        ],
        default=2   
    )
    def __str__(self):
        return f' {self.title}, owner: {self.owner}'


class Booking(models.Model):
    user = models.ForeignKey(BNBUser, on_delete=models.PROTECT)
    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,
        related_name='bookings'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    CHOICES = (
        ('pending', 'Ожидание'),
        ('confirmed', 'Подтверждено'),
        ('canceled', 'Отменено'),
    )
    status = models.CharField(max_length=20,choices=CHOICES, default='pending')
    
