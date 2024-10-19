import scrapy
import json
from ..items import QuoteItem, AuthorItem


class MainSpider(scrapy.Spider):
    name = "main"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def __init__(self, *args, **kwargs):
        super(MainSpider, self).__init__(*args, **kwargs)
        self.quotes_data = []
        self.authors_data = []

    def parse(self, response):
        for quotes in response.xpath("//div[@class='quote']"):
            item = QuoteItem()
            item['quote'] = quotes.xpath(".//span[@class='text']/text()").get().strip()
            item['author'] = quotes.xpath(".//span/small/text()").get().strip()
            item['keywords'] = quotes.xpath(".//div[@class='tags']/a/text()").extract()
            self.quotes_data.append({
                'keywords': item['keywords'],
                'author': item['author'],
                'quote': item['quote']
            })

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
        self.authors_data.append({
            'author': item['fullname'],
            'born_date': item['born_date'],
            'born_location': item['born_location'],
            'description': item['description']
        })

    def close(self, reason):
        
        with open('quotes.json', 'w', encoding='utf-8') as f:
            json.dump(self.quotes_data, f, ensure_ascii=False, indent=2)

        with open('authors.json', 'w', encoding='utf-8') as f:
            json.dump(self.authors_data, f, ensure_ascii=False, indent=2)