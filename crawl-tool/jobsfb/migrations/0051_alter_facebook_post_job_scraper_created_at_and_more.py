# Generated by Django 4.0.2 on 2022-08-19 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsfb', '0050_alter_facebook_post_job_scraper_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebook_post_job_scraper',
            name='created_at',
            field=models.FloatField(default=1660931222.697687),
        ),
        migrations.AlterField(
            model_name='facebook_post_job_scraper',
            name='timestamp',
            field=models.FloatField(default=1660931222.697673),
        ),
        migrations.AlterField(
            model_name='facebook_post_job_scraper',
            name='updated_at',
            field=models.FloatField(default=1660931222.697693),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_job_scraper',
            name='created_at',
            field=models.FloatField(default=1660931222.698235),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_job_scraper',
            name='updated_at',
            field=models.FloatField(default=1660931222.698244),
        ),
    ]
