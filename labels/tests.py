# -*- coding:utf-8 -*-

from django.test import TestCase
from users.models import TaskUser

from .models import Label


class LabelsTest(TestCase):
    def setUp(self):
        self.user = TaskUser.objects.create_user(
            username='user1',
            password='TestTestTest1',
        )
        self.client.force_login(self.user)
        Label.objects.create(name='test')

    def test_create(self):
        response = self.client.post('/labels/create/', {'name': 'test1'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), 2)

    def test_update(self):
        response = self.client.post('/labels/1/update/', {'name': 'test2'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), 1)

    def test_delete(self):
        response = self.client.post('/labels/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Label.objects.count(), 0)
