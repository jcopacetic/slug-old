from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

# from slugs.achievements.models import Achievement, UserAchievement
from slugs.dashboard.models import Dashboard  # Setting

# from slugs.pets.models import Slug, UserSlug
from slugs.wallet.models import Ledger, Wallet

# from slugs.items.models import Inventory, Shop


User = get_user_model()


@receiver(post_save, sender=User)
def init_user(sender, instance, created, **kwargs):
    if created:
        dashboard = Dashboard.objects.create(user=instance)
        # inventory = Inventory.objects.create(dashboard=dashboard)
        # shop = Shop.objects.create(dashboard=dashboard)
        wallet = Wallet.objects.create(dashboard=dashboard)
        ledger = Ledger.objects.create(wallet=wallet)
        ledger.add_balance(300)
        # chest = Item.objects.get
