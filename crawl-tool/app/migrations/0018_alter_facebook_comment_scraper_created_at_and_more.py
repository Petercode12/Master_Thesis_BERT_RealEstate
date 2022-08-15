# Generated by Django 4.0.2 on 2022-08-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_facebook_comment_scraper_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='created_at',
            field=models.FloatField(default=1660494302.600038),
        ),
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='timestamp',
            field=models.FloatField(default=1660494302.60003),
        ),
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494302.600043),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='created_at',
            field=models.FloatField(default=1660494302.599131),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='timestamp',
            field=models.FloatField(default=1660494302.599119),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494302.599137),
        ),
        migrations.AlterField(
            model_name='facebook_reaction_scraper',
            name='created_at',
            field=models.FloatField(default=1660494302.600456),
        ),
        migrations.AlterField(
            model_name='facebook_reaction_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494302.600464),
        ),
        migrations.AlterField(
            model_name='facebook_user_from_group_scraper',
            name='created_at',
            field=models.FloatField(default=1660494302.601275),
        ),
        migrations.AlterField(
            model_name='facebook_user_from_group_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494302.601282),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_scraper',
            name='created_at',
            field=models.FloatField(default=1660494302.600899),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494302.600906),
        ),
        migrations.AlterField(
            model_name='facebook_user_scraper',
            name='created_at',
            field=models.FloatField(default=1660494302.599443),
        ),
        migrations.AlterField(
            model_name='facebook_user_scraper',
            name='updated_at',
            field=models.FloatField(default=1660494302.599451),
        ),
    ]
