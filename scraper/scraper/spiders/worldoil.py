import scrapy

class WorldOilSpider(scrapy.Spider):
    name = 'worldoil_spider'
    allowed_domains = ['worldoil.com']
    start_urls = [
    # 'https://worldoil.com/news/2024/1/22/libya-restarts-production-exports-from-country-s-largest-oil-field/',
    # 'https://worldoil.com/news/2024/2/26/libya-resumes-wafa-oil-field-operations-following-protests/',
    # 'https://worldoil.com/news/2024/1/8/trio-petroleum-restarts-production-from-california-s-mccool-ranch-oil-field/',
    # 'https://worldoil.com/news/2024/2/15/eni-to-fast-track-natural-gas-discovery-development-offshore-cypress-following-successful-production-test/',
    # 'https://worldoil.com/news/2023/4/18/alberta-regulator-reconsiders-suncor-oil-sands-expansion/',
    'https://worldoil.com/news/2022/7/11/suncor-energy-replacing-ceo-after-oil-sands-mine-fatality/',
    ]

    def parse(self, response):
        # Extract the title using the CSS selector for the <h1> tag within the 'news-detail-title' class
        title = response.css('.news-detail-title h1::text').get()
        publication_date = response.css('.news-detail-date::text').get()
        author = response.css('.news-detail-author::text').get()
        # Extract all the paragraphs using the CSS selector for <p> tags within the 'news-detail-content' class
        # This assumes that advertisement divs do not contain <p> tags
        paragraphs = response.css('.news-detail-content p::text').getall()
        article_text = '\n'.join(paragraphs)

        # Return the extracted title and paragraphs
        yield {
            'title': title,
            'publication_date': publication_date,
            'author': author,
            'article_text': article_text
        }
