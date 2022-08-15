from django.core.management.base import BaseCommand
from configuration.config import Config
from django.conf import settings
import subprocess
from asyncio.subprocess import PIPE
import os.path

cfg = Config("configuration/config.json")


class Command(BaseCommand):
            

    help = 'Crontab for Crawling ViecLamTot'

    # def read_input(self, inputfile):
    #     f = open(settings.CORE_DIR + f'/jobs/{inputfile}')
    #     keywords = f.readline().strip()
    #     page = f.readline().strip()
    #     return keywords, page

    # def add_arguments(self, parser):
    #     parser.add_argument(
    #         '-i',
    #         '--inputfile',
    #         default='vieclam_input.txt',
    #         dest= 'inputfile'
    #     )

        # parser.add_argument(
        #     '-k',
        #     '--keywords',
        #     default='Data Scientist',
        #     dest='keywords',
        #     # choices=['test']
        #     )

        # parser.add_argument(
        #     '-p',
        #     '--pages',
        #     default='5',
        #     dest='pages',
        #     # choices=['7', '2']
        #     )

    def handle(self, *args, **options):
        # keywords = options['keywords']
        # pages = options['pages']
        
        # inputfile = options['inputfile']
        # keywords, pages = self.read_input(inputfile)
        
        command = (
            # environment_command
            # + " && "
            "cd "
            + str(settings.CORE_DIR)
            + "/vieclamtot_scraper"
            + " && "
        )

        command += (
            'scrapy crawl vieclamtot')

        process = subprocess.Popen(command, shell=True, executable="/bin/bash", stdout=PIPE)
        #subprocess.Popen(command, shell=True)
        # o, e = process.communicate()
        # print(o)
        # with open(os.path.dirname(__file__) + '/../../../cron_ouput.txt', 'wb') as f:
        #     f.write(o)
        #     f.close()
        process.wait()

            
