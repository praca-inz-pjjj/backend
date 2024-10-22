from django.db import models
from backbone.models import CustomUser as User

# models: Classroom UserClassroom Children

class Classroom(models.Model):
    name = models.CharField(unique=True, max_length=100)

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

class Children(models.Model):
    name = models.CharField(max_length=50) # TODO change name to first_name and surname to last_name for it to be compatible with CustomUser model
    surname = models.CharField(max_length=50)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    birth_date = models.DateField(max_length=8)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'surname', 'birth_date'], name='unique_name_surname_birth_date')
        ]
        verbose_name = "Child" # "Dziecko"
        verbose_name_plural = "Children" # "Dzieci"

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.name, self.surname)
        return full_name.strip()
