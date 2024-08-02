from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import string
import random
def generate_unique_code(length=6):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choices(characters, k=length))
    while User.objects.filter(referral_code=code).exists():
        code = ''.join(random.choices(characters, k=length))
    return code

class User(AbstractUser):
    telegram_id = models.CharField(max_length=100, unique=True)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    nickname = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    referral_code = models.CharField(max_length=100, null=True, blank=True)
    start_farming = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True)

    # Отключение групп и разрешений, если они не нужны
    groups = models.ManyToManyField(Group, related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions', blank=True)

    # Удаление полей, связанных с паролем
    password = None
    first_name = None
    last_name = None
    email = None

    def set_password(self, raw_password):
        # Отключение установки пароля
        pass

    def check_password(self, raw_password):
        # Отключение проверки пароля
        return False

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = generate_unique_code()
        super().save(*args, **kwargs)

class GlobalTask(models.Model):
    task_name = models.CharField(max_length=255)
    task_description = models.TextField()
    task_image = models.URLField(max_length=500, null=True, blank=True)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    task_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.task_name

class UserTaskStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(GlobalTask, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'task')

class Referral(models.Model):
    user = models.ForeignKey(User, related_name='referrer', on_delete=models.CASCADE)
    referred_user = models.ForeignKey(User, related_name='referred', on_delete=models.CASCADE)
