# Generated by Django 4.2.1 on 2023-06-23 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('score', models.IntegerField()),
                ('reg_timestamp', models.DateTimeField()),
                ('last_login_timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='barcodes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode', models.CharField(max_length=100)),
                ('product_name', models.CharField(max_length=50)),
                ('product_producer', models.CharField(max_length=100)),
                ('product_description', models.CharField(max_length=200)),
            ],
        ),
    ]
