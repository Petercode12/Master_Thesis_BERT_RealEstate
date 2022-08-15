# Generated by Django 4.0.2 on 2022-08-14 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0043_alter_facebook_comment_scraper_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='created_at',
            field=models.FloatField(default=1660495398.244439),
        ),
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='timestamp',
            field=models.FloatField(default=1660495398.244431),
        ),
        migrations.AlterField(
            model_name='facebook_comment_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495398.244445),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='created_at',
            field=models.FloatField(default=1660495398.243503),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='timestamp',
            field=models.FloatField(default=1660495398.243489),
        ),
        migrations.AlterField(
            model_name='facebook_post_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495398.243509),
        ),
        migrations.AlterField(
            model_name='facebook_reaction_scraper',
            name='created_at',
            field=models.FloatField(default=1660495398.244919),
        ),
        migrations.AlterField(
            model_name='facebook_reaction_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495398.244927),
        ),
        migrations.AlterField(
            model_name='facebook_user_from_group_scraper',
            name='created_at',
            field=models.FloatField(default=1660495398.245737),
        ),
        migrations.AlterField(
            model_name='facebook_user_from_group_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495398.245745),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_scraper',
            name='created_at',
            field=models.FloatField(default=1660495398.245365),
        ),
        migrations.AlterField(
            model_name='facebook_user_profile_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495398.245373),
        ),
        migrations.AlterField(
            model_name='facebook_user_scraper',
            name='created_at',
            field=models.FloatField(default=1660495398.243846),
        ),
        migrations.AlterField(
            model_name='facebook_user_scraper',
            name='updated_at',
            field=models.FloatField(default=1660495398.243854),
        ),
    ]
