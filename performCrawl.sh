#!/bin/bash

source bin/activate
pip install -r requirements.txt
FILE_NAME=items-$(date | sed 's/[: ]/\-/g').json
touch $FILE_NAME
scrapy crawl SacredTexts -o $FILE_NAME
