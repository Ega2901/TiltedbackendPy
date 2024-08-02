from django.db import models
import uuid

class User(models.Model):
    telegram_id = models.CharField(max_length=255, unique=True)
    tg_username = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    referral_code = models.CharField(max_length=255, blank=True, null=True, unique=True)
    referrer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tg_username

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='tasks/', null=True, blank=True)
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    task_url = models.URLField(max_length=200, null=True, blank=True)
    points = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name
