import requests
import pandas
import json
import os

from modules.dataADT import Date


class Video:
    """Class for representation information about recorded Twitch stream"""
    def __init__(self, url):
        self.vod_id = url.split('/')[-1]
        self.messages = []
        self.data = {}
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.client_id = config['client_id']

    def _get_vod(self):
        """Get and return general info about video"""
        vod_info = requests.get(
            "https://api.twitch.tv/kraken/videos/v" + self.vod_id,
            headers={"Client-ID": self.client_id}).json()
        self.data = vod_info

    def _get(self, path: str, params: dict = None,
             headers: dict = None) -> requests.Response:
        params = {} if params is None else params
        headers = {} if headers is None else headers
        params['client_id'] = self.client_id

        response: requests.Response = requests.get(
            url=str('https://api.twitch.tv/v5/{}').format(path),
            params=params,
            headers=headers)
        if response.status_code != requests.codes.ok:
            print('\n[Error]')
            print('Twitch API returned status code {}. Please check your'
                  ' client ID.'.format(response.status_code))
            print('\nUrl\t{}\nParams\t{}\nHeaders\t{}\n'.format(response.url,
                                                                params,
                                                                headers))
            exit(1)
        return response

    def _comment_fragment(self, cursor: str = '') -> dict:
        return self._get('videos/{}/comments'.format(self.vod_id),
                         {'cursor': cursor}).json()

    def comments(self):
        """Get all chat messages from recorded video"""
        fragment: dict = {'_next': ''}
        while '_next' in fragment:
            fragment = self._comment_fragment(fragment['_next'])
            for comment in fragment['comments']:
                self.messages.append({'created_at':
                                      Date(comment['created_at'][:-1]),
                                      'commenter_name':
                                          comment['commenter']['display_name'],
                                      'message': comment['message']['body']})

    def write_to_csv(self):
        """Write comments to csv file"""
        if not self.messages:
            self.comments()
        data_time, data_names, data_text = [], [], []

        for mess in self.messages:
            data_time.append(str(mess['created_at']))
            data_names.append(str(mess['commenter_name']))
            data_text.append(mess['message'])

        d1 = pandas.DataFrame(data_time)
        d2 = pandas.DataFrame(data_names)
        d3 = pandas.DataFrame(data_text)
        d = pandas.concat([d1, d2, d3], axis=1)

        outname = '{}.csv'.format(self.vod_id)
        outdir = '../results'
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        outdir += '/{}'.format(self.name())
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        fullname = os.path.join(outdir, outname)
        d.to_csv(fullname)

    # Functions, which return certain info about stream

    def full_name(self):
        if not self.data:
            self._get_vod()
        return self.data['channel']['display_name']

    def name(self):
        if not self.data:
            self._get_vod()
        return self.data['channel']['name']

    def title(self):
        if not self.data:
            self._get_vod()
        return self.data['title']

    def length(self):
        if not self.data:
            self._get_vod()
        return self.data['length']

    def game(self):
        if not self.data:
            self._get_vod()
        return self.data['game']

    def creation_date(self):
        """Returns Date object"""
        if not self.data:
            self._get_vod()
        return Date(self.data['game'])

    def logo(self):
        if not self.data:
            self._get_vod()
        return self.data['logo']

    def banner(self):
        if not self.data:
            self._get_vod()
        return self.data['video-banner']

    def profile_picture(self):
        if not self.data:
            self._get_vod()
        return self.data['profile-banner']

    def description(self):
        if not self.data:
            self._get_vod()
        return self.data['description']

    def views(self):
        if not self.data:
            self._get_vod()
        return self.data['views']

    def followers(self):
        if not self.data:
            self._get_vod()
        return self.data['followers']

    def profile_color(self):
        if not self.data:
            self._get_vod()
        return self.data['profile_banner_background_color']


if __name__ == '__main__':
    video = Video('https://www.twitch.tv/videos/260297159')
    video.write_to_csv()
    print('ds')

