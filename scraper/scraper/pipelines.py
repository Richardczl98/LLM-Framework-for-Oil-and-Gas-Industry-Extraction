# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScraperPipeline:
    def process_item(self, item, spider):
        return item

import os
import string
import logging

class SaveArticlePipeline:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def sanitize_filename(self, filename):
        # Remove invalid file name characters
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        sanitized_filename = ''.join(c for c in filename if c in valid_chars)
        sanitized_filename = sanitized_filename.replace(' ', '_')
        return sanitized_filename[:200]  # Limit file name length

    def process_item(self, item, spider):
        # Sanitize the title to use as a file name
        filename = self.sanitize_filename(item['title']) + '.txt'
        # Create a directory to store the files, if it doesn't exist
        dir_path = 'articles/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        file_path = os.path.join(dir_path, filename)
        self.logger.debug(f"Article saved to {file_path}")

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"Url: {item['url']}\n")
            file.write(f"Title: {item['title']}\n")
            file.write(f"Author: {item['author']}\n")
            file.write(f"Publication date: {item['publication_date']}\n")
            file.write(f"Article Content:\n{item['article_text']}\n")

        return item

