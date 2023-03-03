from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Tank
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

import datetime


def search_tanks(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        tanks = Tank.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Tank.objects.filter(
            date__istartswith=search_str, owner=request.user) | Tank.objects.filter(
            description__icontains=search_str, owner=request.user) | Tank.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = tanks.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    tanks = Tank.objects.filter(owner=request.user)
    paginator = Paginator(tanks, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    #currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'tanks': tanks,
        'page_obj': page_obj,
        #'currency': currency
    }
    return render(request, 'tanks/index.html', context)


@login_required(login_url='/authentication/login')
def add_tank(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'tanks/add_tank.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'tanks/add_tank.html', context)
        description = request.POST['description']
        date = request.POST['tank_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'tanks/add_tank.html', context)

        Tank.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Tank saved successfully')

        return redirect('tanks')


@login_required(login_url='/authentication/login')
def tank_edit(request, id):
    tank = Tank.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'tank': tank,
        'values': tank,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'tanks/edit-tank.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'tanks/edit-tank.html', context)
        description = request.POST['description']
        date = request.POST['tank_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'tanks/edit-tank.html', context)

        tank.owner = request.user
        tank.amount = amount
        tank. date = date
        tank.category = category
        tank.description = description

        tank.save()
        messages.success(request, 'Tank updated  successfully')

        return redirect('tanks')


def delete_tank(request, id):
    tank = Tank.objects.get(pk=id)
    tank.delete()
    messages.success(request, 'Tank removed')
    return redirect('tanks')


def tank_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    tanks = Tank.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(tank):
        return tank.category
    category_list = list(set(map(get_category, tanks)))

    def get_tank_category_amount(category):
        amount = 0
        filtered_by_category = tanks.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in tanks:
        for y in category_list:
            finalrep[y] = get_tank_category_amount(y)

    return JsonResponse({'tank_category_data': finalrep}, safe=False)


def stats_view(request):
    return render(request, 'tanks/stats.html')