# Generated by Django 4.0.4 on 2022-05-09 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_author_options_alter_author_date_of_death_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(blank=True, to='catalog.genre'),
        ),
    ]
