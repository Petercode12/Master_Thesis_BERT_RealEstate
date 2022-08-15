from django.core.management.base import BaseCommand
from facebook_scraper import get_posts
from configuration.config import Config
from django.conf import settings
from app.models import Facebook_Post_Scraper

cfg = Config("configuration/config.json")


class Command(BaseCommand):

    help = 'Crontab for Crawling Facebook Post'
    def add_arguments(self, parser):
        parser.add_argument(
            '-g',
            '--groupID',
            default='hotrosinhvienontapdaicuong',
            dest='groupID',
            # choices=['test']
            )

        parser.add_argument(
            '-p',
            '--pages',
            default='5',
            dest='pages',
            # choices=['7', '2']
            )

    def handle(self, *args, **options):
        group_id = options['groupID']
        pages = int(options['pages'])

        for post in get_posts(
            group=group_id, 
            cookies = str(settings.CORE_DIR)
                + "/facebook_splash_scraper/"
                + cfg.get_facebook_cookie_prefix()
                + str(1)
                + "_backup.json",
            pages = pages,
            options={"allow_extra_requests": False}):
                
                Facebook_Post_Scraper.objects.create(
                    post_message = post['text'],
                    post_image_link = post['image'],
                    post_total_reactions = post['likes'],
                    post_total_comments = post['comments'],
                    post_total_shares = post['shares'],
                    group_id = group_id,
                    post_id =  post['post_id'],
                    post_user_id = post['user_id'],
                    timestamp  = post['time'].timestamp()
                    )

            
