# Generated by Django 4.1.7 on 2023-04-04 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_log_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataExt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Data',
            new_name='DataDetails',
        ),
        migrations.DeleteModel(
            name='Log',
        ),
    ]