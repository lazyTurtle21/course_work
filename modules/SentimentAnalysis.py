from textblob import TextBlob
import re


class Analysor:
    def _clean_text(self, text):
        """
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        """
        return ' '.join(
            re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+) ",
                   " ", text).split())

    def get_sentiment(self, text):
        """
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        """
        analysis = TextBlob(self._clean_text(text))
        polarity = analysis.sentiment.polarity
        if polarity > 0:
            return 'pos', polarity
        elif polarity == 0:
            return 'neut', polarity
        else:
            return 'neg', polarity


if __name__ == "__main__":
    analysor = Analysor()
    print(analysor.get_sentiment('hi sweety KappaPride'))
