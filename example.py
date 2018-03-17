import requests
import pandas
import time


def get_channel_info(channel, client_id):
    url = 'https://api.twitch.tv/kraken/users?login=' + channel
    headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
    data = requests.get(url, headers=headers).json()
    return data


def get_streaming_info(channel_id, client_id):
    url = 'https://api.twitch.tv/kraken/channels/' + channel_id
    headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
    return requests.get(url, headers=headers).json()


def get_vod(vod_id, client_id):
    vod_info = requests.get("https://api.twitch.tv/kraken/videos/v" + vod_id,
                            headers={"Client-ID": client_id}).json()
    return vod_info


def get_messages(vod_id, client_id):
    messages = []
    response = None
    c = 10
    while response is None or '_next' in response:
        query = ('cursor=' + response[
            '_next']) if response is not None and '_next' in response else 'content_offset_seconds=0'
        for i in range(0, 5):
            error = None
            try:
                response = requests.get("https://api.twitch.tv/v5/videos/" + vod_id + "/comments?" + query,
                                        headers={"Client-ID": client_id}).json()
                c -= 1
            except requests.exceptions.ConnectionError as e:
                error = str(e)
            else:
                if "errors" in response or "comments" not in response:
                    error = "error received in chat message response: " + str(response)

            if error is None and c == 0:
                messages += response["comments"]
                return messages


def write_to_csv(messages):
    data_time, data_names, data_text = [], [], []

    for mess in messages:
        data_time.append(mess['created_at'][:-1])
        data_names.append(str(mess['commenter']['name']))
        data_text.append(mess['message']['body'])
    # print(len(data_text), len(data_time), len(data_names), len(messages))
    d1 = pandas.DataFrame(list(set(data_time)))
    d2 = pandas.DataFrame(list(set(data_names)))
    d3 = pandas.DataFrame(list(set(data_text)))
    d = pandas.concat([d1, d2, d3], axis=1)
    d.to_csv('chat.csv')


def main():
    client_secret = '1i3u391r3wyds08klccqlv55oxckdb'
    channel = 'lirik'
    client_id = 'sm19jhp9zr3nnky9xrph351wui00x0'
    general = get_channel_info(channel, client_id)
    print(general)
    channel_id = general['users'][0]['_id']
    stream = get_streaming_info(channel_id, client_id)
    print(stream)

    vod_id = '239338632'
    vod_info = get_vod(vod_id, client_id)
    print(vod_info)
    messages = []
    messages += get_messages(vod_id, client_id)

    print(messages)
    write_to_csv(messages)


if __name__ == '__main__':
    main()
