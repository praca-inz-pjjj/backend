# Generated by Django 5.0.6 on 2024-10-19 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "parent_panel",
            "0003_alter_permission_qr_code_alter_permission_state_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="permission",
            name="state",
            field=models.CharField(
                choices=[
                    ("SLEEP", "Sleep"),
                    ("NOTIFY", "Notify"),
                    ("ACTIVE", "Active"),
                    ("CLOSED", "Closed"),
                    ("PERMANENT", "Permanent"),
                ],
                default="SLEEP",
                max_length=9,
            ),
        ),
    ]