from django.test import TestCase
from eshedule.models import *

class BuildingTestClass(TestCase):
    build = None
    def setUp(self):
        self.build = Building.objects.create(city='Санк-Петербург', address='Новый', number=10, liter='A')

    def testGet(self):
        build1 = Building.objects.filter(address='Новый')
        self.assertEqual(self.build, build1)