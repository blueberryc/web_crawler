from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import csv
import os

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)


class Song_info(object):
    def __init__(self, id):
        self.id = id

    def get_song_info(self):
        url = "https://music.163.com/#/artist?id={0}".format(self.id)
        browser.get(url)
        browser.switch_to.frame('contentFrame')
        # 获取歌手的姓名，并建立对应的文件夹
        artist_name = browser.find_element_by_id("artist-name").text
        print(artist_name)
        path = os.getcwd()+"\\data\\{0}".format(artist_name)
        if not os.path.exists(path):
            os.makedirs(path)

        data = browser.find_element_by_id("hotsong-list").find_elements_by_tag_name("tr")
        song_info = []
        for i in range(len(data)):
            content = data[i].find_element_by_class_name("txt")
            href = content.find_element_by_tag_name("a").get_attribute("href")
            title = content.find_element_by_tag_name("b").get_attribute("title")
            song_info.append((title, href))
        return song_info, path

    def save2csv(self, song_info, path, head=None):
        # 写入模式可以为 'w'，则每次运行时重新写入，'a' 为追加
        with open("{0}/singer{1}.csv".format(path, str(self.id)), 'w', newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if head is not None:
                writer.writerow(head)
            # 写入歌曲信息
            for item in song_info:
                writer.writerow(item)


def main():
    id = 6457
    info = Song_info(id)
    song_info, path = info.get_song_info()
    info.save2csv(song_info, path, head=['song', 'link'])


if __name__ == '__main__':
    main()
