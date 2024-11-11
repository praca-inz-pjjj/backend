from django.db import models
from django.urls import reverse

from backbone.models import CustomUser as User

# models: Classroom UserClassroom Child

class Classroom(models.Model):
    name = models.CharField(unique=True, max_length=100)
    
    def __str__(self):
        return self.name
    
    def get_admin_url(self):
        return reverse("admin:teacher_panel_classroom_change", args=[self.id])
    
    class Meta:
        verbose_name = "Classroom" # "Klasa" 
        verbose_name_plural = "Classrooms" # "Klasy"

class UserClassroom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'classroom'], name='unique_user_classroom')
        ]
        verbose_name = "User-Classroom" # "Klasa Nauczyciela"
        verbose_name_plural = "Users-Classrooms" # "Klasy Nauczyciela"

class Child(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    birth_date = models.DateField(max_length=8)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
    
    def __str__(self):
        return self.get_full_name()
    
    def get_admin_url(self):
        return reverse("admin:teacher_panel_child_change", args=[self.id])
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name', 'last_name', 'birth_date'], name='unique_name_surname_birth_date')
        ]
        verbose_name = "Child" # "Dziecko"
        verbose_name_plural = "Children" # "Dzieci"

