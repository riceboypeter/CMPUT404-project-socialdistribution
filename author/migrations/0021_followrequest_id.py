# Generated by Django 4.1.6 on 2023-04-02 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0020_alter_node_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='FollowRequest',
            name='id',
            field=models.BigAutoField(default='2', primary_key=True, serialize=False),
        ),
    ]
