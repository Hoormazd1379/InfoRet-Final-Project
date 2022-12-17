scrapy crawl medlinePlusGov -o data/medline.json &
scrapy crawl drugscom -o data/drugs.json &
scrapy crawl webMD -o data/webMD.json &