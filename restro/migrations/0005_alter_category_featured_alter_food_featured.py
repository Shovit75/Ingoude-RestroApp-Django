# Generated by Django 5.0.7 on 2024-07-21 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restro', '0004_category_featured_food_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='featured',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='food',
            name='featured',
            field=models.BooleanField(default=True),
        ),
    ]
