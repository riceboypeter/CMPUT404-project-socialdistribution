# Generated by Django 4.1.6 on 2023-04-02 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0019_alter_author_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='url',
            field=models.URLField(default='http://127.0.0.1:8000/', editable=False, max_length=500),
        ),
    ]
