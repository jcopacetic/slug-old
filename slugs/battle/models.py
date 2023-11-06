from django.db import models

from slugs.dashboard.models import Dashboard


class BattleManager(models.Model):
    dashboard = models.OneToOneField(Dashboard, on_delete=models.CASCADE, related_name="battles")

    def __str__(self):
        return f"{self.dashboard.user.username}'s Battle Manager"
