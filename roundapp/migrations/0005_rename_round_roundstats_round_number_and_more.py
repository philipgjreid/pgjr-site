# Generated by Django 5.1.1 on 2024-09-30 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roundapp', '0004_remove_round_player_round_player'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roundstats',
            old_name='round',
            new_name='round_number',
        ),
        migrations.AlterField(
            model_name='roundstats',
            name='sandsave',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'na')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='roundstats',
            name='updown',
            field=models.CharField(blank=True, choices=[('yes', 'Yes'), ('no', 'No'), ('na', 'na')], max_length=50, null=True),
        ),
    ]
