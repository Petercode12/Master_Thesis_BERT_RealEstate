# Generated by Django 4.0.2 on 2022-08-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsfb', '0019_alter_facebook_post_job_scraper_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebook_post_job_scraper',
            name='created_at',
            field=models.FloatField(default=1660494329.891766),
        ),
        migrations.AlterField(
            model_name='facebook_post_job_scraper',
            name='timestamp',
            field=models.FloatField(default=1660494329.891756),
        ),
        migrations.AlterField(
            model_name='facebook_post_job_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494329.891772),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_job_scraper',
            name='created_at',
            field=models.FloatField(default=1660494329.892288),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_job_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494329.892296),
        ),
    ]
