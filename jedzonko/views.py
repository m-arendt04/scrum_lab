import random
from datetime import datetime

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404

from jedzonko.models import Recipe, Recipeplan, Plan, DayName, Page


from django.urls import reverse


class IndexView(View):

    def get(self, request):
        try:
            about_page = Page.objects.get(slug='about')
        except Page.DoesNotExist:
            print("Object does not exist")
            about_page = None
        recipes = Recipe.objects.all()
        n = 3
        recipes_list = random.sample(list(recipes), n)
        ctx = {
            'recipes_1': recipes_list,
            'about_page': about_page,
        }
        return render(request, "index.html", ctx)


class MainView(View):

    def get(self, request):
        recipes = Recipe.objects.count()
        plans = Plan.objects.all().order_by('-created')[0]
        plan_details = Recipeplan.objects.all().filter(plan_id=plans.id)
        ctx = {'recipes': recipes,
               'plans': plans,
               'plan_details': plan_details,
               }
        return render(request, "dashboard.html", ctx)


class RecipesView(View):

    def get(self, request):
        recipes = Recipe.objects.order_by('-votes', '-created')
        page = request.GET.get('page', 1)

        paginator = Paginator(recipes, 50)

        try:
            paginated_recipes = paginator.page(page)
        except PageNotAnInteger:
            paginated_recipes = paginator.page(1)
        except EmptyPage:
            paginated_recipes = paginator.page(paginator.num_pages)

        ctx = {
            'p_recipe': paginated_recipes,
        }

        return render(request, "app-recipes.html", ctx)


class SchedulesView(View):

    def get(self, request):
        schedules = Plan.objects.order_by('name')
        page = request.GET.get('page', 1)
        paginator = Paginator(schedules, 50)

        try:
            paginated_schedules = paginator.page(page)
        except PageNotAnInteger:
            paginated_schedules = paginator.page(1)
        except EmptyPage:
            paginated_schedules = paginator.page(paginator.num_pages)

        ctx = {
            'p_schedules': paginated_schedules
        }
        return render(request, "app-schedules.html", ctx)


class AddRecipeView(View):

    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        recipe_name = request.POST.get("recipe_name")
        recipe_desc = request.POST.get("recipe_description")
        time = request.POST.get("time")
        preparation = request.POST.get("preparation")
        ingredients = request.POST.get("ingredients")

        if recipe_name and recipe_desc and time and preparation and ingredients:
            new_recipe = Recipe()
            new_recipe.name = recipe_name
            new_recipe.description = recipe_desc
            new_recipe.preparation_time = time
            new_recipe.preparation = preparation
            new_recipe.ingredients = ingredients
            new_recipe.save()
            return redirect("recipes")
        context = {"prompt": "Wypełnij poprawnie wszystkie pola"}
        return render(request, 'app-add-recipe.html', context)


class AddPlanView(View):

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        plan_name = request.POST.get("plan_name")
        plan_desc = request.POST.get("plan_description")

        if plan_name and plan_desc:
            new_plan = Plan()
            new_plan.name = plan_name
            new_plan.description = plan_desc
            new_plan.save()
            request.session['plan_id'] = new_plan.id
            return redirect("plan_add_details")
        context = {"prompt": "Wypełnij poprawnie wszystkie pola"}
        return render(request, 'app-add-schedules.html', context)


class RecipeDetails(View):

    def get(self, request):
        recipe_id = request.GET.get('recipe_id')
        current_recipe = Recipe.objects.get(pk=recipe_id)
        ingredients = current_recipe.ingredients.split(' ')
        ing_with_quantity = []
        for i in range(len(ingredients) - 1):
            if i % 2 == 0:
                ing_with_quantity.append(ingredients[i] + ' ' + ingredients[i + 1])

        ctx = {
            'current_recipe': current_recipe,
            'ingredients': ing_with_quantity,
        }
        return render(request, 'app-recipe-details.html', ctx)

    def post(self, request):
        if request.method == "POST":
            recipe_id = request.POST.get('recipe_id')
            vote = request.POST.get('vote')
            int_vote = int(vote)
            voted_recipe = Recipe.objects.get(pk=recipe_id)
            if isinstance(int_vote, int):
                voted_recipe.votes = voted_recipe.votes + int_vote
                voted_recipe.save()
                return redirect('/recipe?recipe_id={}'.format(recipe_id))
            else:
                return HttpResponse('Do głosowania użyj liczby!')


class PlanDetails(View):

    def get(self, request):
        plan_id = request.session.get('plan_id')
        if not plan_id:
            raise Http404
        plans = Plan.objects.get(pk=plan_id)
        recipes = Recipe.objects.all()
        days = DayName.objects.all()
        ctx = {
            'plan_title': plans,
            # 'plans': plans,
            'plan_id': plan_id,
            'recipes': recipes,
            'days': days,
        }
        return render(request, "app-schedules-meal-recipe.html", ctx)

    def post(self, request):
        plan_id = request.POST.get("plan_id")
        # plan = request.POST.get("plan")
        meal_name = request.POST.get("meal_name")
        meal_number = request.POST.get("meal_number")
        recipe = request.POST.get("recipe")
        day = request.POST.get("day")
        current_session = request.session.get('plan_id')
        plan_id = int(plan_id)
        if plan_id == current_session:
            relevant_plan = Plan.objects.get(pk=plan_id)
            relevant_day = DayName.objects.get(pk=day)
            relevant_recipe = Recipe.objects.get(name=recipe)
            new_recipe_plan = Recipeplan()
            new_recipe_plan.meal_name = meal_name
            new_recipe_plan.order = meal_number
            new_recipe_plan.plan_id = relevant_plan
            new_recipe_plan.day_name_id = relevant_day
            new_recipe_plan.recipe_id = relevant_recipe
            new_recipe_plan.save()
            return redirect("plan_add_details")
        else:
            raise Http404


class NewPlanDetails(View):

    def get(self, request):
        try:
            request.session.pop('plan_id')
            request.session.modified = True
            return render(request, 'app-schedules-meal-recipe2.html')
        except KeyError:
            raise Http404

    def post(self, request):
        return redirect('schedules')


class PlanParticulars(View):

    def get(self, request, id):
        plans = Plan.objects.get(pk=id)
        plan_details = Recipeplan.objects.all().filter(plan_id=plans.id)
        ctx = {
            'plans': plans,
            'plan_details': plan_details,
        }
        return render(request, "app-details-schedules.html", ctx)


class ModifyRecipe(View):

    def get(self, request, id):
        try:
            edited_recipe = Recipe.objects.get(pk=id)
            ctx = {
                'edited_recipe': edited_recipe
            }
            return render(request, 'app-edit-recipe.html', ctx)

        except:
            raise Http404

    def post(self, request, id):
        recipe_id = request.POST.get('recipe_id')
        edited_recipe = Recipe.objects.get(pk=recipe_id)

        for key, value in request.POST.items():
            if value == '':
                ctx = {
                    'edited_recipe': edited_recipe,
                    'message': 'Wypełnij poprawnie wszystkie pola',
                }
                return render(request, 'app-edit-recipe.html', ctx)

        new_recipe = Recipe()
        new_recipe.name = request.POST.get('recipe_name')
        new_recipe.description = request.POST.get('recipe_description')
        new_recipe.preparation_time = request.POST.get('recipe_time')
        new_recipe.preparation = request.POST.get('recipe_preparation')
        new_recipe.ingredients = request.POST.get('recipe_ingredients')
        new_recipe.save()

        return redirect('recipes')

