# -*- coding:utf-8 -*-

from django.test import TestCase

from .models import TaskUser


class UsersTest(TestCase):
    def setUp(self):
        self.user = TaskUser.objects.create_user(
            username='user1',
            password='TestTestTest1',
        )
        self.client.force_login(self.user)

    def test_register(self):
        response = self.client.post(
            '/users/create/',
            {
                'first_name': 'user2',
                'last_name': 'user2',
                'username': 'user2',
                'password1': 'TestTestTest1',
                'password2': 'TestTestTest1',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskUser.objects.count(), 2)

    def test_update(self):
        response = self.client.post(
            '/users/1/update/',
            {
                'first_name': 'user1',
                'last_name': 'user1',
                'username': 'user1',
                'password1': 'TestTestTest1',
                'password2': 'TestTestTest1',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskUser.objects.count(), 1)

    def test_delete(self):
        response = self.client.post('/users/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(TaskUser.objects.count(), 0)
