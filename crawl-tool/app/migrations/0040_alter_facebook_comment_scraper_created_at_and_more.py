# Generated by Django 4.0.2 on 2022-08-14 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_alter_facebook_comment_scraper_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='created_at',
            field=models.FloatField(default=1660495333.811182),
        ),
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='timestamp',
            field=models.FloatField(default=1660495333.811174),
        ),
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495333.811188),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='created_at',
            field=models.FloatField(default=1660495333.810267),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='timestamp',
            field=models.FloatField(default=1660495333.810253),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495333.810273),
        ),
        migrations.AlterField(
            model_name='facebook_reaction_scraper',
            name='created_at',
            field=models.FloatField(default=1660495333.811625),
        ),
        migrations.AlterField(
            model_name='facebook_reaction_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495333.811634),
        ),
        migrations.AlterField(
            model_name='facebook_user_from_group_scraper',
            name='created_at',
            field=models.FloatField(default=1660495333.812482),
        ),
        migrations.AlterField(
            model_name='facebook_user_from_group_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495333.812505),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_scraper',
            name='created_at',
            field=models.FloatField(default=1660495333.812118),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495333.812126),
        ),
        migrations.AlterField(
            model_name='facebook_user_scraper',
            name='created_at',
            field=models.FloatField(default=1660495333.810599),
        ),
        migrations.AlterField(
            model_name='facebook_user_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495333.810607),
        ),
    ]
