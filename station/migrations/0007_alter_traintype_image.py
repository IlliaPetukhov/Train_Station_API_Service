# Generated by Django 4.1 on 2024-11-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('station', '0006_alter_traintype_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traintype',
            name='image',
            field=models.ImageField(blank=True, upload_to='train_types'),
        ),
    ]