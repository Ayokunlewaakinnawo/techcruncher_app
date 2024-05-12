# Generated by Django 5.0.3 on 2024-03-30 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=255)),
                ('desc', models.TextField()),
                ('url', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('author', models.TextField(max_length=255)),
                ('body', models.TextField()),
                ('image1', models.ImageField(blank=True, upload_to='images/')),
                ('image2', models.ImageField(blank=True, upload_to='images/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-date_added'],
            },
        ),
    ]
