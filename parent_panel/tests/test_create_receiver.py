import json
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from unittest.mock import patch
from backbone.models import CustomUser, Log
from teacher_panel.models import Child, Classroom
from parent_panel.models import PermittedUser, UserChild
from backbone.types import LogType

class CreateReceiverTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parent_user = CustomUser.objects.create_user(
            email='parent@test.com',
            password='testpass',
            parent_perm=2,
            first_name = 'Parent',
            last_name = 'User',
        )
        self.classroom = Classroom.objects.create(name='Test Classroom')
        self.child = Child.objects.create(
            first_name='Test',
            last_name='Child',
            classroom=self.classroom,
            birth_date='2018-01-01',
        )
        UserChild.objects.create(user=self.parent_user, child=self.child)
        self.valid_payload = {
            "first_name": "Jan",
            "second_name": "Zieliński",
            "email": "janziel@test.com",
            "phone": "123429789",
            "password": "password123",
        }
        self.url = reverse('create_receiver', args=[self.child.id])

    def test_invalid_json_returns_bad_request(self):
        self.client.force_authenticate(user=self.parent_user)
        response = self.client.post(self.url, data="invalid data", content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_child_not_found_returns_400(self):
        self.client.force_authenticate(user=self.parent_user)
        url = reverse('create_receiver', args=[999])
        response = self.client.post(url, data=self.valid_payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_not_parent_of_child_returns_400(self):
        other_parent = CustomUser.objects.create_user(
            email='other@test.com',
            password='paspaspas',
            parent_perm=2,
            first_name ='Parent 2',
            last_name ='User',
        )
        self.client.force_authenticate(user=other_parent)
        response = self.client.post(self.url, data=self.valid_payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)


    def test_successful_user_creation_returns_200(self):
        self.client.force_authenticate(user=self.parent_user)
        response = self.client.post(self.url, data=json.dumps(self.valid_payload), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'], self.valid_payload['email'])
        self.assertTrue(CustomUser.objects.filter(email=self.valid_payload['email']).exists())
        self.assertTrue(PermittedUser.objects.filter(child=self.child).exists())
