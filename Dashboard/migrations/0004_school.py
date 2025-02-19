# Generated by Django 5.1.6 on 2025-02-19 14:41

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0003_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('npsn', models.CharField(max_length=8, unique=True)),
                ('nama_sekolah', models.CharField(max_length=100)),
                ('alamat', models.TextField()),
                ('kota', models.CharField(max_length=50)),
                ('provinsi', models.CharField(max_length=50)),
                ('kode_pos', models.CharField(max_length=5)),
                ('telepon', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('kepala_sekolah', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('AKTIF', 'Aktif'), ('TIDAK_AKTIF', 'Tidak Aktif')], default='AKTIF', max_length=11)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('guru', models.ForeignKey(blank=True, limit_choices_to={'role': 'GURU'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sekolah', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sekolah',
                'verbose_name_plural': 'Sekolah',
                'db_table': 'sekolah',
            },
        ),
    ]
