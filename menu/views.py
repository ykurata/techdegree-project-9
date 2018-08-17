from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from operator import attrgetter
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


def menu_list(request):
    """Show a list of menus which expiration_date is future date or blank"""
    menus = Menu.objects.prefetch_related(
        'items'
    ).filter(
        Q(expiration_date__isnull=True)|
        Q(expiration_date__gte=timezone.now())
    ).order_by(
        '-expiration_date'
    )
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})


def menu_detail(request, pk):
    """Show a menu detail"""
    menu = Menu.objects.prefetch_related(
        'items'
    ).get(
        pk=pk
    )
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    """Show an item detail"""
    item = Item.objects.select_related(
        'chef'
    ).prefetch_related(
        'ingredients'
    ).get(
        pk=pk
    )
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    """Create a new menu view"""
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            # Save many to many field
            form.save_m2m()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})


def edit_menu(request, pk):
    """Edit a menu view"""
    menu = get_object_or_404(Menu, pk=pk)
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=menu.pk)
    return render(request, 'menu/menu_edit.html', {'form': form})
