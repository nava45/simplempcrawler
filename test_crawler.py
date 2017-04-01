import unittest
import requests

from crawler import parse_html


class CrawlerTest(unittest.TestCase):
    def setUp(self):
        self.urls = ['https://news.ycombinator.com/news', 'https://pymotw.com/2/unittest/']

    def test_parse(self):
        for url in self.urls:
            page = requests.get(url).content
            if 'ycombinator' in url:
                self.assertFalse(parse_html(page))
            else:
                self.assertTrue(parse_html(page))

 
if __name__ == '__main__':
    unittest.main()
