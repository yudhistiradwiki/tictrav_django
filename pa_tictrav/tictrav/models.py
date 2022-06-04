from django.conf import settings
from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
"""
    Kelas untuk mengatur pembuatan akun
"""
class AuthManager(BaseUserManager):
    """
        Pembuatan Akun User (Registrasi)
    """
    def create_user(self, email, password, full_name=None, age=None, location=None):
        if not email:
            raise ValueError("Kolom email tidak boleh kosong")
        if not password:
            raise ValueError("Kolom password tidak boleh kosong")

        email = self.normalize_email(email)
        user = self.model(email=email, 
                          full_name=full_name, 
                          age=age,
                          location=location)
        
        user.set_password(password)
        user.save()
        return user

    """
        Pembuatan Akun Admin
    """
    def create_superuser(self, email, password, **other_fields):
        user = self.create_user(
                email=self.normalize_email(email),
                password=password,
            )
        user.is_admin = True
        user.is_staff=True
        user.is_superuser=True
        user.save()
        return user

"""
    Abstrak kelas untuk akun
"""
class AccountCustom(AbstractBaseUser):
    email = models.EmailField(verbose_name=_("email"),max_length=254, unique=True)
    full_name = models.CharField(max_length=300, unique=True, null=True)
    age = models.IntegerField(null=True)
    location = models.TextField(null=True)
    created = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = AuthManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label ):
        return True


"""
    Tabel Primari
"""
class TourismPlace(models.Model):
    place_id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    place_name = models.TextField()
    description = models.TextField()
    category = models.TextField()
    city = models.TextField()
    price = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    time_minutes = models.IntegerField(default=0)
    lat = models.FloatField()
    long = models.FloatField()
    img = models.ImageField(upload_to='images/',default="images/no_img.jpg")
    
    def __str__(self):
        return "{}".format(self.place_id)


"""
    Tabel Sekunder
"""
class Reservation(models.Model):
    class StatusOption(models.TextChoices):
        PROCESS = "Dalam Proses",
        FINISH = "Selesai"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.ForeignKey(TourismPlace, on_delete=models.CASCADE)
    place_ratings = models.IntegerField(default=0)
    status = models.CharField(max_length=100,choices=StatusOption.choices,default=StatusOption.PROCESS)
    time = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
      return "{} {} {}".format(self.user, self.place, self.place_ratings)


class personalization(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.TextField()

    def __str__(self):
      return "{} {} ".format(self.user_Id, self.category)
    

