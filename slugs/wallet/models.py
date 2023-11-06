from django.db import models, transaction
from django.db.utils import IntegrityError

from slugs.dashboard.models import Dashboard
from slugs.game.options import TRANSACTION_TYPE


class Wallet(models.Model):
    dashboard = models.OneToOneField(Dashboard, on_delete=models.CASCADE, related_name="wallet")
    balance = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dashboard.user.username}'s Wallet"


class Ledger(models.Model):
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE, related_name="ledger")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.wallet.dashboard.user.username}'s Ledger"

    def add_balance(self, amount):
        if not self.wallet:
            raise ValueError("No wallet associated with this ledger.")
        try:
            with transaction.atomic():
                ledger_item = LedgerItem.objects.create(ledger=self, action=1, amount=amount)
                ledger_item.save()
                self.wallet.balance = models.F("balance") + amount
                self.wallet.save()
        except IntegrityError as e:
            # Handle database integrity errors
            raise e
        except Exception as e:
            # Handle other exceptions (e.g., database connection issues)
            raise e

    def subtract_balance(self, amount):
        if not self.wallet:
            raise ValueError("No wallet associated with this ledger.")

        if self.wallet.balance < amount:
            raise ValueError("Insufficient balance.")

        try:
            with transaction.atomic():
                ledger_item = LedgerItem.objects.create(ledger=self, action=2, amount=amount)
                ledger_item.save()
                self.wallet.balance = models.F("balance") - amount
                self.wallet.save()
        except IntegrityError as e:
            # Handle database integrity errors
            raise e
        except Exception as e:
            # Handle other exceptions (e.g., database connection issues)
            raise e


class LedgerItem(models.Model):
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name="items")
    action = models.CharField(max_length=3, choices=TRANSACTION_TYPE)
    amount = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_action_display()} {self.amount}G"
