# Generated by Django 3.1 on 2020-08-16 04:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_userforeignkey.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Zoom',
            fields=[
                ('idAccount', models.CharField(default=None, max_length=255)),
                ('firstName', models.CharField(default=None, max_length=255)),
                ('lastName', models.CharField(default=None, max_length=255)),
                ('email', models.EmailField(db_index=True, max_length=254, primary_key=True, serialize=False, unique=True)),
                ('meetingId', models.CharField(default=None, max_length=255)),
                ('personalMeetingUrl', models.CharField(default=None, max_length=255)),
                ('user', django_userforeignkey.models.fields.UserForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('user',),
            },
        ),
    ]
