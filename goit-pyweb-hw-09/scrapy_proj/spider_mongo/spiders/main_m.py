import scrapy
from scrapy.crawler import CrawlerProcess
from spider_mongo.items import QuoteItem, AuthorItem
from scrapy.utils.project import get_project_settings



class MainSpider(scrapy.Spider):
    name = "main_m"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for quotes in response.xpath("//div[@class='quote']"):
            item = QuoteItem()
            item['quote'] = quotes.xpath(".//span[@class='text']/text()").get().strip()
            item['author'] = quotes.xpath(".//span/small/text()").get().strip()
            item['keywords'] = quotes.xpath(".//div[@class='tags']/a/text()").extract()
            yield item

            author_url = quotes.xpath("span/a/@href").get()
            if author_url:  
                yield scrapy.Request(url=response.urljoin(author_url), callback=self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=response.urljoin(next_link), callback=self.parse)

    def parse_author(self, response):
        self.log(f"Parsing author details from: {response.url}")
        item = AuthorItem()
        author = response.xpath("//div[@class='author-details']")
        item['fullname'] = response.xpath("//h3[@class='author-title']/text()").get().strip()
        item['born_date'] = response.xpath("//span[@class='author-born-date']/text()").get().strip()
        item['born_location'] = response.xpath("//span[@class='author-born-location']/text()").get().strip()
        item['description'] = response.xpath("//div[@class='author-description']/text()").get().strip()
        yield item
        
process = CrawlerProcess(get_project_settings())
process.crawl(MainSpider)
process.start()