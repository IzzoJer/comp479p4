import scrapy
from bs4 import BeautifulSoup as bs


class ConcordiaSpider(scrapy.Spider):
    name = 'concordiaSpider'
    allowed_domains = ['concordia.ca']
    start_urls = ['https://www.concordia.ca/']

    def parse(self, response):

        soup = bs(response.text, 'html.parser')
        text = soup.find('section', {'id' : 'content-main'}).text
        text = text.replace('\n', '')
        yield {response.request.url : text}

        rejectList = ['.jpg', '.pdf', '.xml', '.mp3']

        for x in response.css('a::attr(href)').extract():
            if x[-4:] not in rejectList and '/fr/' not in x:
                x = response.urljoin(x)
                yield response.follow(x, callback=self.parse)





