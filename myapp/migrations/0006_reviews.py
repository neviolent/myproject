# Generated by Django 4.2.1 on 2023-06-23 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_remove_account_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_id', models.IntegerField(default=0)),
                ('product_barcode', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
    ]
