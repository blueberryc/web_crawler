import requests
import json
import re
import urllib.request
import Singer
import pandas as pd


class WYmusic(object):
    def __init__(self, song_name, song_id, path):
        self.song_name = song_name
        self.song_id = song_id
        self.path = path

    def get_lyric(self):
        url = 'http://music.163.com/api/song/lyric?' + 'id=' + str(self.song_id) + '&lv=1&kv=1&tv=-1'
        r = requests.get(url)
        json_obj = r.text
        j = json.loads(json_obj)
        lyric = j['lrc']['lyric']
        # 利用正则表达式去除时间轴
        regex = re.compile(r'\[.*\]')
        final_lyric = re.sub(regex, '', lyric)
        return final_lyric

    def get_mp3(self):
        url = 'http://music.163.com/song/media/outer/url?id=' + str(self.song_id)+'.mp3'
        try:
            print("正在下载：{0}".format(self.song_name))
            urllib.request.urlretrieve(url, '{0}/{1}.mp3'.format(self.path, self.song_name))
            print("Finish...")
        except:
            print("Fail...")

    def write_text(self):
        lyric = self.get_lyric()
        print("正在写入歌曲：{0}".format(self.song_name))
        print(lyric)
        with open("{0}/{1}.txt".format(self.path, self.song_name), 'w', encoding='utf-8') as f:
            f.write(lyric)


def downloader(singer_id):
    # 将歌曲信息写入文件
    info = Singer.Song_info(singer_id)
    song_info, path = info.get_song_info()
    info.save2csv(song_info, path, head=['song', 'link'])
    print(song_info, path)
    print('{0}\\singer{1}.csv'.format(path, singer_id))
    # 根据歌曲信息获取歌词和mp3
    info = pd.read_csv('{0}\\singer{1}.csv'.format(path, singer_id), engine='python', encoding='utf-8')
    for index, row in info.iterrows():
        song = row['song']
        regex = re.compile(r'id=.*')
        link = re.search(regex, row['link']).group()[3:]
        music = WYmusic(song, link, path)
        music.write_text()
        music.get_mp3()


def test():
    links = "https://music.163.com/song?id=413829644"
    regex = re.compile(r'id=.*')
    link = re.search(regex, links)
    print(link.group())


def main():
    downloader(1050282)


if __name__ == '__main__':
    main()
