import scrapy 
import random
from fake_useragent import UserAgent
ua = UserAgent()
ua.random
import scrapy_proxies

class Amazon(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = ['https://www.amazon.com/s?k=jackets+for+women&crid=9EM4YPNRPEB1&sprefix=jackets%2Caps%2C589&ref=nb_sb_ss_i_1_7']

    def parse(self, response):
        #First portion scrapes LISTS
        #looks for href urls to scrape the details on their pages and not the root page itself
        urls = response.css("a.a-link-normal.a-text-normal::attr(href)").extract()
        #Join then Visits the scraped URLS
        for url in urls: 
            #this finds the last half of a url and joins it to the base url
            #OLD LINE: url = response.urljoin(url)
            url = "https://www.amazon.com"+url
            #now it yields all the completed urls contained in the root page and parses their details
            yield scrapy.Request(url=url, callback=self.parse_details)

        #Scrapes data:
        for item in response.css('div.sg-col-4-of-24.sg-col-4-of-12.sg-col-4-of-36.s-result-item.sg-col-4-of-28.sg-col-4-of-16.sg-col.sg-col-4-of-20.sg-col-4-of-32'):
            item = {
                'detail 1': item.css('div.pathway').extract(),
                'detail 2': item.css('div.pathway').extract(),
            }
            yield item


        #follow pagination links
        next_page_url = response.css('li.next > a::attr(href)').extract_first()
        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    def parse_details(self, response):
        yield {
            'detail 1': response.css('div.detail::text').extract(),
            'detail 2': response.xpath('xpath').extract(),
        }



