import pytz
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Dashboard(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="dashboard")
    exp = models.IntegerField(default=0)
    lvl = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Dashboard"


timezone_choices = [(tz, tz) for tz in pytz.all_timezones]


class Setting(models.Model):
    dashboard = models.OneToOneField(Dashboard, on_delete=models.CASCADE, related_name="settings")
    timezone = models.CharField(max_length=63, choices=timezone_choices, default="UTC")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dashboard.user.username}' Settings"
