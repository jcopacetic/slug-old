from django.db import models

from slugs.dashboard.models import Dashboard
from slugs.game.options import ACHIEVEMENT_OPTIONS


class Gallery(models.Model):
    dashboard = models.OneToOneField(Dashboard, on_delete=models.CASCADE, related_name="gallery")

    def __str__(self):
        return f"{self.dashboard.user.username}'s Gallery"


class Achievement(models.Model):
    type = models.CharField(max_length=2, choices=ACHIEVEMENT_OPTIONS)
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=800)
    reward_exp = models.IntegerField(null=True, blank=True)
    limit = models.IntegerField(default=1)

    def get_avatar_url(self):
        return f"images/achievements/{self.id}.png"

    def award_items(self):
        pass


class UserAchievement(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="assigned")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
