from django.db import models


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(null=True)
    preparation = models.TextField(null=True)


class Page(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.CharField(max_length=255)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


days = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
)

class DayName(models.Model):
    day_name = models.IntegerField(choices=days)
    order = models.IntegerField()


class Recipeplan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()
    day_name_id = models.ForeignKey(DayName, on_delete=models.CASCADE)
    plan_id = models.ForeignKey(Plan, on_delete=models.CASCADE)
    recipe_id = models.ForeignKey(Recipe, on_delete=models.CASCADE)



