# Generated by Django 4.1.7 on 2023-03-28 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_db', to='home.database'),
        ),
    ]
