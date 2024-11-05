from datetime import datetime

from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.db import migrations
from .. import types

def add_demo_data(apps, schema_editor):
    CustomUser = apps.get_model('backbone', 'CustomUser')
    # Consent = apps.get_model('backbone', 'Consent')
    # UserConsent = apps.get_model('backbone', 'UserConsent')

    Classroom = apps.get_model('teacher_panel', 'Classroom')
    UserClassroom = apps.get_model('teacher_panel', 'UserClassroom')
    Child = apps.get_model('teacher_panel', 'Child')

    UserChild = apps.get_model('parent_panel', 'UserChild')
    # History = apps.get_model('parent_panel', 'History')
    PermittedUser = apps.get_model('parent_panel', 'PermittedUser')
    Permission = apps.get_model('parent_panel', 'Permission')

    admin = CustomUser(first_name="Jan", last_name="Kowalski", email="admin@mail.pl", phone_number="123456789", is_staff=True, is_active=True, 
                       teacher_perm=types.AccessType.FULL, parent_perm=types.AccessType.FULL, is_superuser=True, password=make_password("12345"))
    admin.save()
    teacher = CustomUser(first_name="Piotr", last_name="Nowak", email="teacher@mail.pl", phone_number="738294752", is_staff=True, is_active=True, 
                         teacher_perm=types.AccessType.FULL, parent_perm=types.AccessType.NONE, is_superuser=False, password=make_password("12345"))
    teacher.save()
    issuer = CustomUser(first_name="Krzysztof", last_name="Woźniak", email="issuer@mail.pl", phone_number="", is_staff=True, is_active=True, 
                        teacher_perm=types.AccessType.PARTIAL, parent_perm=types.AccessType.NONE, is_superuser=False, password=make_password("12345"))
    issuer.save()
    parent = CustomUser(first_name="Jakub", last_name="Zieliński", email="parent@mail.pl", phone_number="", is_staff=False, is_active=True, 
                        teacher_perm=types.AccessType.NONE, parent_perm=types.AccessType.FULL, is_superuser=False, password=make_password("12345"))
    parent.save()
    parent2 = CustomUser(first_name="Andrzej", last_name="Kamiński", email="parent2@mail.pl", phone_number="", is_staff=False, is_active=True, 
                         teacher_perm=types.AccessType.NONE, parent_perm=types.AccessType.FULL, is_superuser=False, password=make_password("12345"))
    parent2.save()
    receiver = CustomUser(first_name="Jakub", last_name="Lewandowski", email="receiver@mail.pl", phone_number="", is_staff=False, is_active=True, 
                          teacher_perm=types.AccessType.NONE, parent_perm=types.AccessType.PARTIAL, is_superuser=False, password=make_password("12345"))
    receiver.save()
    receiver2 = CustomUser(first_name="Tomasz", last_name="Wiśniewski", email="receiver2@mail.pl", phone_number="", is_staff=False, is_active=True, 
                           teacher_perm=types.AccessType.NONE, parent_perm=types.AccessType.PARTIAL, is_superuser=False, password=make_password("12345"))
    receiver2.save()

    classroom1 = Classroom(name="Skrzaty 2a")
    classroom1.save()
    classroom2 = Classroom(name="Kreciki 1b")
    classroom2.save()
    classroom3 = Classroom(name="Truskawki 1a")
    classroom3.save()
    UserClassroom.objects.create(user=teacher, classroom=classroom1)
    UserClassroom.objects.create(user=teacher, classroom=classroom2)
    UserClassroom.objects.create(user=teacher, classroom=classroom3)

    child1 = Child(first_name="Filip", last_name="Sobiesiak", classroom=classroom1, birth_date=datetime(2017, 1, 1))
    child1.save()
    child2 = Child(first_name="Dariusz", last_name="Chełmiński", classroom=classroom1, birth_date=datetime(2017, 5, 15))
    child2.save()
    child3 = Child(first_name="Wioletta", last_name="Malcharek", classroom=classroom1, birth_date=datetime(2017, 6, 19))
    child3.save()
    child4 = Child(first_name="Nikola", last_name="Berkowska", classroom=classroom2, birth_date=datetime(2018, 10, 25))
    child4.save()
    child5 = Child(first_name="Maja", last_name="Śmietana", classroom=classroom2, birth_date=datetime(2018, 3, 30))
    child5.save()
    child6 = Child(first_name="Gracjan", last_name="Gralak", classroom=classroom2, birth_date=datetime(2018, 11, 13))
    child6.save()
    child7 = Child(first_name="Blanka", last_name="Kulikova", classroom=classroom3, birth_date=datetime(2018, 7, 5))
    child7.save()
    child8 = Child(first_name="Borys", last_name="Kluza", classroom=classroom3, birth_date=datetime(2018, 12, 27))
    child8.save()
    child9 = Child(first_name="Mieczysław", last_name="Duży", classroom=classroom3, birth_date=datetime(2018, 2, 9))
    child9.save()
    UserChild.objects.create(user=parent, child=child1)
    UserChild.objects.create(user=parent2, child=child2)
    UserChild.objects.create(user=parent2, child=child3)
    UserChild.objects.create(user=parent, child=child4)
    UserChild.objects.create(user=parent, child=child5)

    permitteduser1 = PermittedUser.objects.create(user=parent, child=child1, parent=parent, date=timezone.now(), signature_delivered=True)
    permitteduser1.save()
    permitteduser2 = PermittedUser.objects.create(user=parent2, child=child2, parent=parent2, date=timezone.now(), signature_delivered=True)
    permitteduser2.save()
    permitteduser3 = PermittedUser.objects.create(user=parent2, child=child3, parent=parent2, date=timezone.now(), signature_delivered=True)
    permitteduser3.save()
    permitteduser4 = PermittedUser.objects.create(user=parent, child=child4, parent=parent, date=timezone.now(), signature_delivered=True)
    permitteduser4.save()
    permitteduser5 = PermittedUser.objects.create(user=parent, child=child5, parent=parent, date=timezone.now(), signature_delivered=True)
    permitteduser5.save()
    permitteduser6 = PermittedUser.objects.create(user=receiver, child=child1, parent=parent, date=timezone.now(), signature_delivered=False)
    permitteduser6.save()
    permitteduser7 = PermittedUser.objects.create(user=receiver, child=child4, parent=parent, date=timezone.now(), signature_delivered=False)
    permitteduser7.save()
    permitteduser8 = PermittedUser.objects.create(user=receiver2, child=child2, parent=parent2, date=timezone.now(), signature_delivered=False)
    permitteduser8.save()
    Permission.objects.create(permitteduser=permitteduser1, parent=parent, state=types.PermissionState.PERMANENT , end_date=timezone.now())
    Permission.objects.create(permitteduser=permitteduser2, parent=parent2, state=types.PermissionState.PERMANENT , end_date=timezone.now())
    Permission.objects.create(permitteduser=permitteduser3, parent=parent2, state=types.PermissionState.PERMANENT , end_date=timezone.now())
    Permission.objects.create(permitteduser=permitteduser4, parent=parent, state=types.PermissionState.PERMANENT , end_date=timezone.now())
    Permission.objects.create(permitteduser=permitteduser5, parent=parent, state=types.PermissionState.PERMANENT , end_date=timezone.now())


class Migration(migrations.Migration):

    dependencies = [
        ('backbone', '0001_initial'),
        ('parent_panel', '0001_initial'),
        ('teacher_panel', '0001_initial')
    ]

    operations = [
        migrations.RunPython(add_demo_data),
    ]