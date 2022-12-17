import scrapy
import time

class drugsCom(scrapy.Spider):
    name = "drugscom"

    start_urls = [
        'https://www.drugs.com/drug_information.html'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 2 # 2 seconds of delay
        }

    def parse(self, response):
        for l in response.css('nav.ddc-paging ul li'):
            next_page = l.css('a::attr(href)').get()
            next_page = response.urljoin(next_page)
            print('NEXT PAGE IS: ' + next_page)
            time.sleep(0.5)
            yield scrapy.Request(next_page, callback=self.parse_medpage)

    def parse_medpage(self, response):
        print('PARSING: ' + response.url)
        for l in response.css('ul.ddc-list-column-2 li'):
            next_page = l.css('a::attr(href)').get()
            next_page = response.urljoin(next_page)
            time.sleep(0.5)
            yield scrapy.Request(next_page, callback=self.parse_medpage_drug)
            # yield {
            #     'name' : l.css('a::text').get(),
            #     'addr' : l.css('a::attr(href)').get()
            # }
    
    def parse_medpage_drug(self, response):
        name = response.css('div.contentBox h1::text').get()
        desc = response.css('div.contentBox p::text').getall()
        source = response.url
        yield {
            'name' : name,
            'description' : desc,
            'source' : source
        }

class medlinePlusGov(scrapy.Spider):
    name = 'medlinePlusGov'

    start_urls = [
        'https://medlineplus.gov/druginformation.html'
    ]

    def parse(self, response):
        for l in response.css('ul.alpha-links li'):
            next_page = l.css('a::attr(href)').get()
            next_page = response.urljoin(next_page)
            print('NEXT PAGE IS: ' + next_page)
            yield scrapy.Request(next_page, callback=self.parse_medpage)

    def parse_medpage(self, response):
        print('PARSING: ' + response.url)
        for l in response.css('ul#index li'):
            next_page = l.css('a::attr(href)').get()
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_medpage_drug)

    def parse_medpage_drug(self, response):
        name = response.css('div.page-title h1::text').get()
        source = response.url
        sections = []
        for sec in response.css('article section div'):
            sections.append(
                {
                    'title' : sec.css('div .section-title h2::text').get(),
                    'text' : sec.css('div .section-body p::text').getall()
                }
            )
        yield {
            'name' : name,
            'description' : sections,
            'source' : source
        }

class webMD(scrapy.Spider):
    name = 'webMD'

    start_urls = [
        'https://www.webmd.com/drugs/2/index'
    ]

    def parse(self, response):
        for l in response.css('ul.browse-letters li'):
            next_page = l.css('a::attr(href)').get()
            next_page = response.urljoin(next_page)
            print('NEXT PAGE IS: ' + next_page)
            yield scrapy.Request(next_page, callback=self.parse_sub)

    def parse_sub(self, response):
        for l in response.css('ul.browse-letters.squares.sub-alpha li.sub-alpha-square'):
            next_page = l.css('a::attr(href)').get()
            next_page = response.urljoin(next_page)
            print('NEXT PAGE IS: ' + next_page)
            yield scrapy.Request(next_page, callback=self.parse_medpage)

    def parse_medpage(self, response):
        print('PARSING: ' + response.url)
        for l in response.css('div.drugs-search-list-conditions ul li'):
            next_page = l.css('a::attr(href)').get()
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse_medpage_drug)

    def parse_medpage_drug(self, response):
        name = response.css('h1.drug-name::text').get()
        source = response.url
        sections = []
        for sec in response.css('div.tab-content'):
            sections.append(
                {
                    'title' : sec.css('div.title-bg h2::text').get(),
                    'text' : sec.css('div.monograph-content p::text').getall()
                }
            )
        yield {
            'name' : name,
            'description' : sections,
            'source' : source
        }