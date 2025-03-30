from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from backbone.models import CustomUser, Log
from parent_panel.models import Permission, PermittedUser
from backbone.types import PermissionState, LogType
from teacher_panel.models import Child, Classroom

class GenerateQRCodeTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.parent_user = CustomUser.objects.create_user(
            email='parent@test.com',
            password='testpass',
            parent_perm=2,
            first_name = 'Parent',
            last_name = 'User',
        )
        self.receiver =  CustomUser.objects.create_user(
            email='receiver@test.com',
            password='testpass',
            parent_perm=1,
            first_name ='Receiver',
            last_name ='User',
        )
        self.classroom = Classroom.objects.create(name='Test Classroom')
        self.child = Child.objects.create(
            first_name='Test',
            last_name='Child',
            classroom=self.classroom,
            birth_date='2018-01-01',
        )
        self.permission = Permission.objects.create(
            permitteduser=PermittedUser.objects.create(user=self.receiver, child=self.child, parent=self.parent_user),
            parent=self.receiver,
            start_date=timezone.now() - timedelta(days=1),
            end_date=timezone.now() + timedelta(days=1),
            state=PermissionState.ACTIVE
        )
        self.url = reverse('generate_QR_code', kwargs={'id': self.permission.id})
        self.client.force_authenticate(user=self.receiver)

    def test_generate_qr_code_success(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('qr_code', response.data)
        self.permission.refresh_from_db()
        self.assertEqual(self.permission.qr_code, response.data['qr_code'])
        self.assertEqual(self.permission.state, PermissionState.ACTIVE)

    def test_permission_closed(self):
        self.permission.state = PermissionState.CLOSED
        self.permission.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_418_IM_A_TEAPOT)
        self.assertEqual(response.data['data'], "This permission is already closed")

    def test_too_early_to_generate_qr_code(self):
        self.permission.start_date = timezone.now() + timedelta(days=1)
        self.permission.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)
        self.assertEqual(response.data['data'], "Too early to generate QR Code")

    def test_permission_expired(self):
        self.permission.end_date = timezone.now() - timedelta(days=1)
        self.permission.save()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_412_PRECONDITION_FAILED)
        self.assertEqual(response.data['data'], "This permission has expired")
        self.permission.refresh_from_db()
        self.assertEqual(self.permission.state, PermissionState.CLOSED)