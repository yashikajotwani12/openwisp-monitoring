# Generated by Django 2.0.2 on 2018-03-01 13:37

import collections
import uuid

import django.db.models.deletion
import django.utils.timezone
import jsonfield.fields
import model_utils.fields
import swapper
from django.db import migrations, models

from ..settings import CHECK_CLASSES


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        swapper.dependency('config', 'Device', '0004_add_device_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'created',
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='created',
                    ),
                ),
                (
                    'modified',
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name='modified',
                    ),
                ),
                ('name', models.CharField(db_index=True, max_length=64)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('description', models.TextField(blank=True, help_text='Notes')),
                (
                    'object_id',
                    models.CharField(blank=True, db_index=True, max_length=36),
                ),
                (
                    'check',
                    models.CharField(
                        choices=CHECK_CLASSES,
                        db_index=True,
                        help_text='Select check type',
                        max_length=128,
                        verbose_name='check type',
                    ),
                ),
                (
                    'params',
                    jsonfield.fields.JSONField(
                        blank=True,
                        default=dict,
                        dump_kwargs={'indent': 4},
                        help_text='parameters needed to perform the check',
                        load_kwargs={'object_pairs_hook': collections.OrderedDict},
                        verbose_name='parameters',
                    ),
                ),
                (
                    'content_type',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to='contenttypes.ContentType',
                    ),
                ),
            ],
            options={
                'abstract': False,
                'swappable': swapper.swappable_setting('check', 'Check'),
            },
        )
    ]
