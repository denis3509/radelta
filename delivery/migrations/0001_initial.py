# Generated by Django 4.2.6 on 2023-10-23 19:22

import django.db.models.deletion
from django.db import migrations, models

import delivery.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=200)),
                ('weight', models.DecimalField(decimal_places=3, max_digits=6, validators=[delivery.models.more_than_zero])),
                ('cost', models.DecimalField(decimal_places=2, max_digits=6, validators=[delivery.models.more_than_zero])),
                ('delivery_cost', models.DecimalField(decimal_places=2, max_digits=6, null=True, validators=[delivery.models.more_than_zero])),
                ('registration_status', models.TextField(choices=[('SUCCESS', 'Success'), ('FAILURE', 'Failure')], default='PENDING')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sessions.session')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='delivery.packagetype')),
            ],
        ),
    ]