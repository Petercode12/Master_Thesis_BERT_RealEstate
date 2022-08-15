#!/bin/bash
SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`
echo $PWD
cd /code/vieclamtot_scraper
echo $PWD
# cd "$SCRIPTPATH"
# cd "../../.."
. /opt/env/bin/activate
scrapy crawl vieclamtot
# cd /vieclamtot_scraper
# scrapy crawl vieclamtot
# date > last_update.txt