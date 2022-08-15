# Generated by Django 4.0.2 on 2022-08-14 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_facebook_comment_scraper_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='created_at',
            field=models.FloatField(default=1660494274.419675),
        ),
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='timestamp',
            field=models.FloatField(default=1660494274.419667),
        ),
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494274.419681),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='created_at',
            field=models.FloatField(default=1660494274.418725),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='timestamp',
            field=models.FloatField(default=1660494274.418711),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494274.418732),
        ),
        migrations.AlterField(
            model_name='facebook_reaction_scraper',
            name='created_at',
            field=models.FloatField(default=1660494274.420127),
        ),
        migrations.AlterField(
            model_name='facebook_reaction_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494274.420135),
        ),
        migrations.AlterField(
            model_name='facebook_user_from_group_scraper',
            name='created_at',
            field=models.FloatField(default=1660494274.420926),
        ),
        migrations.AlterField(
            model_name='facebook_user_from_group_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494274.420949),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_scraper',
            name='created_at',
            field=models.FloatField(default=1660494274.420555),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494274.420563),
        ),
        migrations.AlterField(
            model_name='facebook_user_scraper',
            name='created_at',
            field=models.FloatField(default=1660494274.419065),
        ),
        migrations.AlterField(
            model_name='facebook_user_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494274.419073),
        ),
    ]
