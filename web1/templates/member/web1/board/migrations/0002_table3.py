# Generated by Django 2.2.5 on 2020-01-06 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table3',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('hei', models.IntegerField()),
                ('wei', models.IntegerField()),
                ('age', models.IntegerField()),
            ],
        ),
    ]
