from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.urls import reverse

from backbone.models import CustomUser as User
from teacher_panel.models import Child
from backbone.types import PermissionState

# models: UserChild, History, PermittedUser, Permission

class UserChild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'child'], name='unique_parent_child')
        ]
        verbose_name = "User-Child" # "Dziecko Użytkownika"
        verbose_name_plural = "Users-Children" # "Dzieci Użytkownika"

class History(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='receiver')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher')
    decision = models.BooleanField(default=True)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "History" # "Historia"
        verbose_name_plural = "History" # "Historia"
        ordering = ['-date']

class PermittedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="parent")
    date = models.DateTimeField(default=timezone.now)
    signature_delivered = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
    
    def get_admin_url(self):
        return reverse("admin:parent_panel_permitteduser_change", args=[self.id])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'child'], name='unique_receiver_child'),
        ]
        verbose_name = "PermittedUser" # "Dozwolony Użytkownik"
        verbose_name_plural = "PermittedUsers" # "Dozwoleni Użytkownicy"

class Permission(models.Model):
    permitteduser = models.ForeignKey(PermittedUser, on_delete=models.CASCADE)
    parent = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=11, choices=PermissionState.choices, default=PermissionState.SLEEP)
    qr_code = models.IntegerField(null=True, blank=True) #TODO validator so it accepts only 8-number integers
    two_factor_code = models.IntegerField(null=True, blank=True) #TODO validator so it accepts only 8-number integers
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()   

    class Meta:
        verbose_name = "Permission" # "Uprawnienie"
        verbose_name_plural = "Permissions" # "Uprawnienia"
