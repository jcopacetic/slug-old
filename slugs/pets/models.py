from django.db import models
from django.utils.text import slugify

from slugs.dashboard.models import Dashboard
from slugs.game.models import Set
from slugs.game.options import COLOR_OPTIONS, TYPE_OPTIONS


class SlugManager(models.Model):
    dashboard = models.OneToOneField(Dashboard, on_delete=models.CASCADE, related_name="slugs")

    def __str__(self):
        return f"{self.dashboard.user.username}'s Slug Manager"


class Move(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=800)
    type_1 = models.CharField(max_length=2, choices=TYPE_OPTIONS, default=11)
    type_2 = models.CharField(max_length=2, choices=TYPE_OPTIONS, null=True, blank=True)
    damage = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    set = models.ForeignKey(Set, on_delete=models.PROTECT, related_name="moves")
    rarity = models.IntegerField(default=0)
    probability = models.DecimalField(default=1.0, decimal_places=1, max_digits=2)

    release_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def get_avatar_url(self):
        return f"images/moves/{self.name}.gif"


class Slug(models.Model):
    name = models.CharField(max_length=20)
    type_1 = models.CharField(max_length=2, choices=TYPE_OPTIONS, default=11)
    type_2 = models.CharField(max_length=2, choices=TYPE_OPTIONS, null=True, blank=True)
    set = models.ForeignKey(Set, on_delete=models.PROTECT, related_name="slugs")
    rarity = models.IntegerField(default=0)
    probability = models.DecimalField(default=1.0, decimal_places=1, max_digits=2)

    release_date = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    def get_avatar_url(self):
        return f"images/slugs/slug-{slugify(self.id)}.gif"


class UserSlug(models.Model):
    manager = models.ForeignKey(SlugManager, on_delete=models.CASCADE, null=True, blank=True, related_name="slugs")
    pet_name = models.CharField(max_length=20, null=True, blank=True)
    color = models.CharField(max_length=2, choices=COLOR_OPTIONS, default=1)
    moves = models.ManyToManyField(Move, blank=True, related_name="slugs")
    exp = models.IntegerField(default=0)
    lvl = models.IntegerField(default=0)
    in_battle = models.BooleanField(default=False, null=True, blank=True)
    favorite = models.BooleanField(default=False, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pet_name}"

    def get_avatar_url(self):
        return f"images/slugs/slug-{slugify(self.id)-{self.color}}.gif"

    def set_favorite(self):
        if self.manager.slugs.filter(in_battle=True).count() == 0:
            user_pets = self.manager.slugs.all()
            for item in user_pets:
                if item.favorite is True:
                    item.favorite = False
                    item.save()
            self.favorite = True
            self.save()


class PetStat(models.Model):
    pet = models.OneToOneField(UserSlug, on_delete=models.CASCADE, related_name="stats")
    hp_now = models.IntegerField(default=0)
    hp_total = models.IntegerField(default=0)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    special_attack = models.IntegerField(default=0)
    special_defense = models.IntegerField(default=0)
    accuracy = models.IntegerField(default=0)
    evasion = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.pet.pet_name}'s stats"


# health
# health_regeneration
# Armor
# Magic Resistance
# Movement Speed
# attack Range
# Attack Speed
# Base Attack Speed
# Attack Animation
# Attack Ratio
# Bonus Attack Speed
# Unit Radius
# gameplay Radius
# selection radius
# pathing radius
# acquisition radius
# Special Statistics
# damage Dealt bonus
# damage received bonus
# healing bonus
