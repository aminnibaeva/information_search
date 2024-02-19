import os
import shutil
import urllib.request

from bs4 import BeautifulSoup


class WebCrawler:

    def __init__(self,
                 starting_url,
                 max_page_count=100,
                 output_dir="results/",
                 output_file="index.txt"):
        self.starting_url = starting_url
        self.nested_link_class = "reference internal"
        self.max_page_count = max_page_count
        self.output_dir = output_dir
        self.output_file = output_file
        self.current_page_index = 0
        self.queue = []
        self.processed_urls = set()

    def initiate_crawling(self):
        self.prepare_output_directory()
        self.queue.append(self.starting_url)

        while self.queue and self.current_page_index < self.max_page_count:
            url = self.queue.pop()
            html_content = self.retrieve_html(url)
            soup = BeautifulSoup(html_content, 'html.parser')

            print(f'Processing {self.current_page_index} {url} ...')

            self.save_html(self.current_page_index, url, html_content)
            self.processed_urls.add(url)
            self.current_page_index += 1
            nested_links = list(filter(self.is_not_processed, self.extract_nested_links(soup)))
            self.queue.extend(nested_links)

    def prepare_output_directory(self):
        shutil.rmtree(self.output_dir)
        os.mkdir(self.output_dir)

    def is_not_processed(self, url):
        return url not in self.processed_urls

    def extract_nested_links(self, soup):
        internal_references = soup.find_all("a", class_=self.nested_link_class)
        links = [self.starting_url + item['href'] for item in internal_references]
        return links

    def save_html(self, index, url, html_content):
        html_file_path = os.path.join(self.output_dir, f"{index}.html")
        with open(html_file_path, "wb") as html_file:
            html_file.write(html_content)

        output_file_path = os.path.join(self.output_dir, self.output_file)
        with open(output_file_path, 'a') as file:
            line = f"{index} – {url}\n"
            file.write(line)

    def retrieve_html(self, current_url):
        response = urllib.request.urlopen(current_url)
        return response.read()