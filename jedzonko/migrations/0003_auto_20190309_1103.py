# Generated by Django 2.1.2 on 2019-03-09 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0002_recipe_preparation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='votes',
            field=models.IntegerField(null=True),
        ),
    ]
