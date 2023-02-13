# Generated by Django 3.1.6 on 2023-02-13 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0002_auto_20230212_1924'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('url', models.URLField(editable=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=500)),
                ('private', models.BooleanField(default=False)),
                ('content_type', models.CharField(choices=[('text/markdown', 'markdown'), ('text/plain', 'plain'), ('image/jpeg', 'image')], default='text/plain', max_length=20)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='author.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('url', models.URLField(editable=False)),
                ('comment', models.TextField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
    ]
