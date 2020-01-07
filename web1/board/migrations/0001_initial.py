# Generated by Django 2.2.5 on 2020-01-06 00:25

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table1',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('writer', models.CharField(max_length=50)),
                ('hit', models.IntegerField()),
                ('img', models.BinaryField(null=True)),
                ('regdate', models.DateTimeField(auto_now_add=True)),
            ],
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Table2',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('kor', models.IntegerField()),
                ('eng', models.IntegerField()),
                ('math', models.IntegerField()),
                ('regdate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
