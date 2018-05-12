from __future__ import print_function, unicode_literals
from bs4 import BeautifulSoup as BS4

import requests


def decimal_filter(text):
    """Extract decimal from text.
    """
    res = list()
    for char in text:
        if char in "1234567890.":
            res.append(char)
    if len(res) > 0:
        return float("".join(res))
    else:
        return None


class SentimentAnalysis:
    def __init__(self):
        self.request_url = "http://text-processing.com/demo/sentiment/"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/"
                          "537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 "
                          "Safari/537.36",
            "Referer": "http://text-processing.com/demo/sentiment/",
        }

    def http_post(self, text):
        """Make a http post to "http://text-processing.com/demo/sentiment/",
        get their analysis result, return the html text.

        They use utf-8 encoding.
        """
        try:
            res = requests.post(self.request_url, headers=self.header,
                                data={"language": "english", "text": text})
            return res.text
        except:
            return None

    def extract(self, html):
        """Extract polarity and positive score from html.
        """
        polarity, score = None, None
        try:
            soup = BS4(html, b"lxml")
            # find pos, neg, neutral
            for strong in soup.find_all("strong"):
                try:
                    if strong["class"] == ["large", "positive"]:
                        polarity = "pos"
                    elif strong["class"] == ["large", "negative"]:
                        polarity = "neg"
                    elif strong["class"] == ["large", "quiet"]:
                        polarity = "neutral"
                except:
                    pass

            # find positive value
            try:
                li_positive = soup.find("li", class_="positive")
                score = decimal_filter(li_positive.text)
            except:
                pass

            # fix score when polarity is neutral
            if polarity == "neutral":
                score = 0.5

            return polarity, score
        except:
            return None

    def process(self, text):
        """Return in a tuple tag for text and its strength"""
        return self.extract(processor.http_post(text))


if __name__ == '__main__':
    processor = SentimentAnalysis()
    text = "It helps me saving money"
    print(processor.process(text))  # ('pos', 0.6)
