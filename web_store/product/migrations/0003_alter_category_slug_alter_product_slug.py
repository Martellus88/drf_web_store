# Generated by Django 4.0.6 on 2022-08-02 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
