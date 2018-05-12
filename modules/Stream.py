import requests
import json

from modules.dataADT import Date

"""Добрий день! Пам'ятаєте, я казала, що мені потрібно обговорити свою курсову роботу? На жаль, не змогла бути на консультації в п'ятницю. Чи можна з вами поговорити в будь-який день наступного тижня, але бажано швидше за п'ятницю?"""
class Stream:
    """Class for representation Twitch Stream"""
    def __init__(self, channel_id, client_id):
        """Create new Stream"""
        self.channel = channel_id
        self.client = client_id
        self.data = {}

    def write(self, filename='stream.txt'):
        if not self.data:
            self._get_streaming_info()

        with open(filename, 'w') as file:
            file.write(json.dumps(self.data))

    # Functions, which return certain info about stream

    def name(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['display_name']

    def title(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['title']

    def status(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['status']

    def game(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['game']

    def id(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['_id']

    def creation_date(self):
        """Returns Date object"""
        if not self.data:
            self._get_streaming_info()
        return Date(self.data['game'])

    def logo(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['logo']

    def banner(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['video-banner']

    def profile_picture(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['profile-banner']

    def description(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['description']

    def views(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['views']

    def followers(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['followers']

    def profile_color(self):
        if not self.data:
            self._get_streaming_info()
        return self.data['profile_banner_background_color']

    def _get_streaming_info(self):
        """Gets all info about streaming using Twitch API"""
        url = 'https://api.twitch.tv/kraken/channels/' + self.channel
        headers = {'Client-ID': self.client,
                   'Accept': 'application/vnd.twitchtv.v5+json'}
        self.data = requests.get(url, headers=headers).json()
