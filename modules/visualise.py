import pandas
import matplotlib.pyplot as plt

from SentimentAnalysis import Analysor

analysor = Analysor()


class Visualiser:
    def __init__(self, path):
        self.path = path
        self.polarity = []
        self.time = []

    def readcsv(self):
        file = pandas.read_csv(self.path)
        self.polarity = list(file['0.3'])
        self.time = list(file['0'])

    def visualise(self):
        if not self.time:
            self.readcsv()

        fig = plt.gcf()
        fig.set_size_inches((20, 8), forward=True)
        fig._suptitle = 'Mean Sentiments of Each Minute of the Stream'
        plt.plot(self.time, self.polarity, linewidth=.5)
        plt.xlabel('time')
        plt.ylabel('polarity')
        #fig = plt.gcf()
        #fig.set_size_inches(8, 16)
        #plt.set_title('Mean Sentiments of Each Minute of the Stream')
        #fig.savefig('result.png', dpi=100)
        plt.show()
        plt.savefig('{}.png'.format('result'))


if __name__ == '__main__':
    path = r'D:\python2\course_work\analysis\260481082_vthijshs.csv'
    s = Visualiser(path)
    s.readcsv()
    s.visualise()
