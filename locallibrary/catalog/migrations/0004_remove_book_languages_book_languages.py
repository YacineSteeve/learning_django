# Generated by Django 4.0.4 on 2022-05-08 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_language_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='languages',
        ),
        migrations.AddField(
            model_name='book',
            name='languages',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
    ]
