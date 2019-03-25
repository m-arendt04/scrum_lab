"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jedzonko.views import IndexView, MainView, RecipesView, SchedulesView, AddRecipeView, AddPlanView, RecipeDetails, \
    PlanDetails, PlanParticulars, ModifyRecipe, NewPlanDetails




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='landing_page'),
    path('main/', MainView.as_view(), name='dashboard'),
    path('recipe/list', RecipesView.as_view(), name='recipes'),
    path('schedules/list', SchedulesView.as_view(), name='schedules'),
    path('recipe/add', AddRecipeView.as_view(), name='add_recipe'),
    path('plan/add', AddPlanView.as_view(), name='add_plan'),
    path('recipe', RecipeDetails.as_view(), name='recipe_details'),
    path('plan/<int:id>', PlanParticulars.as_view(), name="plan_particulars"),
    path('recipe/modify/<int:id>', ModifyRecipe.as_view(), name='modify_recipe'),
    path('plan/add/details', PlanDetails.as_view(), name='plan_add_details'),
    path('new_plan_details', NewPlanDetails.as_view(), name='new_plan_details'),
]
