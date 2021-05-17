# -*- coding:utf-8 -*-
from django.test import TestCase
from statuses.models import Status
from users.models import TaskUser

from .filters import TasksFilter
from .models import Task


class TasksTest(TestCase):
    def setUp(self):
        self.user = TaskUser.objects.create_user(
            username='user1',
            password='TestTestTest1',
        )
        self.client.force_login(self.user)
        TaskUser.objects.create_user(
            username='user2',
            password='TestTestTest1',
        )
        Status.objects.create(name='Test')
        Task.objects.create(
            name='Test1',
            description='Test1',
            status=Status.objects.get(name='Test'),
            executor=TaskUser.objects.get(username='user2'),
            creator=self.user,
        )

    def test_create(self):
        response = self.client.post('/tasks/create/', {
            'name': 'Test2',
            'description': 'Test2',
            'status': Status.objects.get(name='Test').id,
            'executor': TaskUser.objects.get(username='user2').id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 2)

    def test_update(self):
        response = self.client.post('/tasks/1/update/', {
            'name': 'Test3',
            'description': 'Test3',
            'status': Status.objects.get(name='Test').id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 1)

    def test_delete(self):
        response = self.client.post('/tasks/1/delete/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)

    def test_filter(self):
        Task.objects.create(
            name='Test2',
            description='Test2',
            status=Status.objects.get(name='Test'),
            executor=TaskUser.objects.get(username='user1'),
            creator=self.user,
        )
        requested_executor = TaskUser.objects.get(username='user1')
        qs = Task.objects.all()
        f = TasksFilter(
            data={'executor': requested_executor},
            queryset=qs,
        )
        filtrated_tasks = f.qs
        expected_tasks = Task.objects.filter(executor=requested_executor)
        self.assertQuerysetEqual(filtrated_tasks, expected_tasks)
