from datetime import datetime
from django.core.urlresolvers import reverse
from django.test import TestCase

from django.contrib.auth.models import User
from django.utils import timezone

from .models import Menu, Item, Ingredient
from .forms import MenuForm


class MenuModelTest(TestCase):
    def test_menu_creation(self):
        menu = Menu.objects.create(
            season = "Summer 2018"
        )
        now = timezone.now()
        self.assertLess(menu.created_date, now)


class ItmeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username = "yasuko"
        )
    def test_item_creation(self):
        item = Item.objects.create(
            name = "test item",
            chef = self.user
        )
        now = timezone.now()
        self.assertLess(item.created_date, now)


class MenuViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username = "yasuko"
        )
        self.item = Item.objects.create(
            name = "test item",
            chef = self.user
        )
        self.menu = Menu.objects.create(
            season = "Test1"
        )
        self.menu.items.add(self.item)

        self.menu2 = Menu.objects.create(
            season = "Test2"
        )
        self.menu2.items.add(self.item)


    def test_menu_list_view(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu, resp.context['menus'])
        self.assertIn(self.menu2, resp.context['menus'])
        self.assertTemplateUsed(resp, 'menu/list_all_current_menus.html')
        self.assertContains(resp, self.menu.season)


    def test_menu_detail_veiw(self):
        resp = self.client.get(reverse('menu_detail',
                                       kwargs={'pk': self.menu.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu, resp.context['menu'])
        self.assertTemplateUsed(resp, 'menu/menu_detail.html')


    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail', kwargs={
                    'pk': self.item.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.item, resp.context['item'])
        self.assertTemplateUsed(resp, 'menu/detail_item.html')


class MenuFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username = "yasuko"
        )
        self.item = Item.objects.create(
            name = "test item",
            chef = self.user
        )
        self.menu = Menu.objects.create(
            season = "Test1"
        )
        self.menu.items.add(self.item)

        self.valid_data = {
            'season':'Summer 2018',
            'items': self.item,
            'expiration_date': '2018-08-31'
        }


    def test_create_menu_view(self):
        resp = self.client.post(reverse('menu_new'), self.valid_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')


    def test_edit_menu_view(self):
        resp = self.client.post(reverse('menu_edit',
                kwargs={'pk': self.menu.pk}), self.valid_data)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'menu/menu_edit.html')
