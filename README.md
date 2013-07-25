growth-hacking-toolkit
======================

The Growth Hacking Toolkit is a collection of growth hacking tools. Enjoy and contribute:)

#Crawlers

##Run the AppAnnie crawler
1. ```cd crawlers/appannie```
2. ```scrapy crawl appannie -a country=united-kingdom -a category=game -a sub_category=brain```

You can pass a number of parameters:
- **country**  
- **category**
- **sub_category**

##Export the results into a csv file
mongoexport --db appannie --csv --collection android_app --fieldFile fields.txt --out contacts.csv

You can filter the results using the query parameter:

mongoexport --db appannie --csv --collection android_app --fieldFile fields.txt --query {min_downloads:{ $gte : 10000} } --out contacts.csv

