# Generated by Django 4.0.2 on 2022-08-21 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobsfb', '0051_alter_facebook_post_job_scraper_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebook_post_job_scraper',
            name='created_at',
            field=models.FloatField(default=1661050580.669352),
        ),
        migrations.AlterField(
            model_name='facebook_post_job_scraper',
            name='timestamp',
            field=models.FloatField(default=1661050580.669337),
        ),
        migrations.AlterField(
            model_name='facebook_post_job_scraper',
            name='updated_at',
            field=models.FloatField(default=1661050580.669383),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_job_scraper',
            name='created_at',
            field=models.FloatField(default=1661050580.670101),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_job_scraper',
            name='updated_at',
            field=models.FloatField(default=1661050580.670118),
        ),
    ]