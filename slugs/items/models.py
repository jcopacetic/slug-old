import random

from django.db import models, transaction
from django.db.utils import IntegrityError
from django.utils.text import slugify

from slugs.dashboard.models import Dashboard
from slugs.game.models import Set
from slugs.game.options import CONSUME_OPTIONS
from slugs.pets.models import Move, Slug, UserSlug


class Inventory(models.Model):
    dashboard = models.OneToOneField(Dashboard, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f"{self.dashboard.user.username}'s Inventory"


class Shop(models.Model):
    dashboard = models.OneToOneField(Dashboard, on_delete=models.CASCADE, related_name="shop")

    def __str__(self):
        return f"{self.dashboard.user.username}'s Shop"


class Item(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=400)
    value = models.IntegerField(default=0)
    set = models.ForeignKey(Set, on_delete=models.PROTECT, related_name="items")
    rarity = models.IntegerField(default=0)
    probability = models.DecimalField(default=1.0, decimal_places=1, max_digits=2)
    release_date = models.DateTimeField(null=True, blank=True)
    retired_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_avatar_url(self):
        return f"images/slugs/slug-{slugify(self.name)}.gif"


class UserItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name="owned")
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name="items")
    in_shop = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.item.name

    def add_to_shop(self):
        try:
            with transaction.atomic():
                ShopItem.objects.create(item=self, shop=self.inventory.dashboard.shop)
                self.in_shop = True
                self.save()
        except IntegrityError as e:
            # Handle database integrity errors
            raise e
        except Exception as e:
            # Handle other exceptions (e.g., database connection issues)
            raise e

    def remove_from_shop(self):
        try:
            with transaction.atomic():
                shopitem = ShopItem.objects.get(item=self)
                shopitem.delete()
                self.in_shop = False
                self.save()
        except IntegrityError as e:
            # Handle database integrity errors
            raise e
        except Exception as e:
            # Handle other exceptions (e.g., database connection issues)
            raise e


class ConsumeItem(UserItem):
    action = models.CharField(max_length=2, choices=CONSUME_OPTIONS)
    amount = models.IntegerField()

    def use_on_slug(self, slug):
        pass

    def use_on_user(self, user):
        pass


class SlugItem(UserItem):
    slug = models.ForeignKey(UserSlug, on_delete=models.PROTECT, null=True, blank=True, related_name="itemized")
    chest = models.BooleanField(default=True)

    def open(self):
        if self.chest:
            slugs = list(Slug.objects.all())

            total_weight = sum(slug.probability for slug in slugs)
            rand = random.uniform(0, total_weight)

            selected_slug = None

            for slug in slugs:
                slug_probability = slug.probability
                if rand < slug_probability:
                    selected_slug = slug
                    break
                rand -= slug_probability

            if selected_slug:
                UserSlug.objects.create(manager=self.inventory.dashboard.slugs)
                self.delete()

    def adopt(self):
        self.slug.manager = self.inventory.dashboard.slugs
        self.slug.save()
        self.delete()


class CurrencyItem(UserItem):
    amount = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        weights = [10] * 250 + [50] * 500 + [10] * 250
        ran = random.choices(range(1, 1001), weights=weights)[0]
        self._meta.get_field("amount").default = ran

    def open(self):
        try:
            with transaction.atomic():
                self.inventory.dashboard.wallet.ledger.add_balance(self.amount)
                self.delete()
        except IntegrityError as e:
            # Handle database integrity errors
            raise e
        except Exception as e:
            # Handle other exceptions (e.g., database connection issues)
            raise e


class MoveItem(UserItem):
    move = models.ForeignKey(Move, on_delete=models.CASCADE, related_name="itemized")

    def __str__(self):
        return self.move.name


class ChestItem(UserItem):
    random_number = models.IntegerField(default=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field("random_number").default = random.randint(2, 5)

    def open(self):
        products = list(Item.objects.all())

        for _ in range(self.random_number):
            total_weight = sum(item.probability for item in products)
            rand = random.uniform(0, total_weight)

            selected_item = None
            for item in products:
                item_probability = item.probability
                if rand < item_probability:
                    selected_item = item
                    break
                rand -= item_probability

            if selected_item:
                if selected_item.id == 1:
                    ChestItem.objects.create(item=selected_item, inventory=self.inventory)
                elif selected_item.id == 2:
                    SlugItem.objects.create(item=selected_item, inventory=self.inventory, chest=True)
                elif selected_item.id == 3:
                    CurrencyItem.objects.create(item=selected_item, inventory=self.inventory)
                else:
                    UserItem.objects.create(item=selected_item, inventory=self.inventory)

        self.delete()


class ShopItem(models.Model):
    item = models.ForeignKey(UserItem, null=True, blank=True, on_delete=models.CASCADE, related_name="for_sale")
    price = models.IntegerField(default=0)
    in_market = models.BooleanField(default=False)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="shop")

    def change_amount(self, amount):
        self.price = amount
        self.save()
