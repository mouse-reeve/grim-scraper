#!/bin/bash

source bin/activate
FILE_NAME=items-$(date | sed 's/[: ]/\-/g').json
touch $FILE_NAME
scrapy crawl SacredTexts -o $FILE_NAME
