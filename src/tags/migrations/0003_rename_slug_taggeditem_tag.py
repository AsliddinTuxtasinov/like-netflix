# Generated by Django 3.2.8 on 2021-10-30 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_taggeditem_object_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taggeditem',
            old_name='slug',
            new_name='tag',
        ),
    ]
