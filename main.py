import os
import re

import nltk
import pymorphy2
from stop_words import get_stop_words

from source.Crawler import WebCrawler

nltk.download('punkt')

morph = pymorphy2.MorphAnalyzer()

stop_words = get_stop_words('ru')


def get_tokens(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        text = re.sub(r'\W+', ' ', text)
        tokens = nltk.word_tokenize(text)
        tokens = [token for token in tokens if token not in stop_words and re.match(r'^[а-яА-Я]+$', token) and not any(
            char.isdigit() for char in token)]
        unique_lemmas = set(tokens)
        return list(unique_lemmas)


def get_lemmas():
    tokens = []

    for filename in os.listdir('results'):
        file_tokens = get_tokens('results/' + filename)
        tokens += file_tokens

    tokens = set(tokens)
    lemmas = {}
    for token in tokens:
        lemma = morph.parse(token)[0].normal_form
        if lemma in lemmas:
            lemmas[lemma].append(token)
        else:
            lemmas[lemma] = [token]

    with open('tokens.txt', 'w', encoding='utf-8') as f:
        for token in sorted(tokens):
            f.write(token + ' ' + '\n')

    with open('lemmas.txt', 'w', encoding='utf-8') as f:
        for lemma in sorted(lemmas.keys()):
            f.write(lemma + ': ' + ', '.join(lemmas[lemma]) + '\n')


if __name__ == '__main__':
    base_url = "https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/bs4ru.html"
    spider = WebCrawler(base_url)
    spider.initiate_crawling()
    get_lemmas()
