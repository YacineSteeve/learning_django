# Generated by Django 4.0.4 on 2022-05-20 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_alter_author_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['last_name', 'first_name', 'date_of_birth', 'date_of_death']},
        ),
    ]
