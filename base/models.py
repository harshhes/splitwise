from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13, null=True, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class ExpenseGroup(models.Model):
    from .utils import ExpenseType

    name = models.CharField(max_length=100, null=True, blank=True)
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=10, choices= (((i.value),(i.value))for i in ExpenseType))
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    image  = models.ImageField(upload_to="images/", null=True, blank=True)
    notes  = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, through="ExpenseParticipant", related_name='participants')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.name}"


class ExpenseParticipant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # user other than payer
    expense = models.ForeignKey(ExpenseGroup, on_delete=models.CASCADE)
    owe_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    percentage = models.DecimalField(max_digits=3, decimal_places=2, default=0.0, null=True, blank=True)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return f'{self.expense}'