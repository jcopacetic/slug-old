from django.db import models


class Set(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=800)
    release_date = models.DateTimeField(null=True, blank=True)
    retired_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} | {self.release_date} - {self.retired_date}"
