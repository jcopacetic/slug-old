# Generated by Django 4.2.5 on 2023-09-09 09:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("dashboard", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Achievement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "type",
                    models.CharField(
                        choices=[(1, "account"), (2, "items"), (3, "shop"), (4, "market"), (5, "slugs"), (6, "user")],
                        max_length=2,
                    ),
                ),
                ("name", models.CharField(max_length=80)),
                ("description", models.TextField(max_length=800)),
                ("reward_exp", models.IntegerField(blank=True, null=True)),
                ("limit", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Gallery",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "dashboard",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, related_name="gallery", to="dashboard.dashboard"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserAchievement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "achievement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assigned",
                        to="achievements.achievement",
                    ),
                ),
                (
                    "gallery",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="achievements",
                        to="achievements.gallery",
                    ),
                ),
            ],
        ),
    ]
