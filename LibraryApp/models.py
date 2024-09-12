from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from datetime import date

# Create your models here.
class CustomUser(AbstractUser):

    user_type=models.CharField(default=1,max_length=10)
    status=models.IntegerField(default=0)
    

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.category_name
    
class Libraryuser(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    age=models.IntegerField()
    number=models.CharField(max_length=255)

class Books(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    book_name=models.CharField(max_length=255)
    auther_name=models.CharField(max_length=255)
    bpid=models.IntegerField(null=True,blank=True)
    stocks=models.IntegerField(null=True,blank=True)
    price=models.IntegerField(null=True,blank=True)
    img = models.ImageField(blank=True, upload_to="image/", null=True)



from datetime import timedelta
from django.utils import timezone

# class Rentalhistory(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
#     book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
#     rent_date = models.DateField()
#     due_date = models.DateField(null=True, blank=True)
#     fine_amount = models.IntegerField(null=True, blank=True)
#     return_status = models.CharField(max_length=255, null=True, blank=True)
#     payment_status = models.CharField(max_length=255, null=True, blank=True)
#     issue_reported = models.BooleanField(default=False)
#     reported_at = models.DateTimeField(null=True, blank=True)
#     fine_payed = models.IntegerField(null=True, blank=True)

class Rentalhistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    rent_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    fine_amount = models.IntegerField(null=True, blank=True)
    return_status = models.CharField(max_length=255, null=True, blank=True)
    payment_status = models.CharField(max_length=255, null=True, blank=True)
    issue_reported = models.BooleanField(default=False)
    reported_at = models.DateTimeField(null=True, blank=True)
    fine_payed = models.IntegerField(null=True, blank=True)
    returned_date = models.DateTimeField(null=True, blank=True)


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)  # Updated from 'prod'
    quantity = models.IntegerField(default=1)
    def total_price(self):
        return self.quantity * self.book.price  # Updated from 'self.prod.price'

class Purchasehistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)
    purchase_date = models.DateField(default=timezone.now)
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(null=True, blank=True)
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.book.price
        super().save(*args, **kwargs)

    
class ReportBookIssue(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, null=True)  # Directly link to Books model
    book_price = models.DecimalField(max_digits=10, decimal_places=2)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f'Report by {self.user} for {self.book}'
    

    

    
