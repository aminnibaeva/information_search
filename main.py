from source.Crawler import WebCrawler

if __name__ == '__main__':
    base_url = "https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/bs4ru.html"
    spider = WebCrawler(base_url)
    spider.initiate_crawling()
