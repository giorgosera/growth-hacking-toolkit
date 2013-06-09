growth-hacking-toolkit
======================

The Growth Hacking Toolkit is a collection of growth hacking tools. Enjoy and contribute:)

#Crawlers

##Run the AppAnnie crawler
scrapy crawl appannie -a country=united-states -a category=health-and-fitness

##Export the results into a csv file
mongoexport --db appannie --csv --collection android_app --fieldFile fields.txt --out contacts.csv

