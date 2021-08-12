#!/usr/bin/python3
# encoding=utf-8

import os
import sys
import json
import time
from ffmpy import FFmpeg
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

SAVE_PATH = "E://test"


def main():
    domain = "https://www.hifini.com/"
    page_idx = -1
    soup = BeautifulSoup('', features='html.parser')
    while True:
        page_idx += 1
        for idx in range(7, 1024, 2):
            music_data = soup.select(
                "#body > div > div > div.col-lg-9.main > div > div.card-body > ul > li:nth-child(%d)" % (idx))

            idx += 1
            if len(music_data) == 0:
                page_url = "https://www.hifini.com/forum-1-%d.htm?orderby=lastpid" % int(page_idx)
                logging.info("try request %s" % page_url)
                while True:
                    response = requests.get(page_url)  # Get方式获取网页数据
                    if response.status_code != 200:
                        logging.warning("request failed, code=%d" % response.status_code)
                        time.sleep(1)
                    else:
                        break
                soup = BeautifulSoup(response.text, features='html.parser')
                break
            elif len(music_data) != 1:
                continue

            data_href = music_data[0].get('data-href')
            url = domain + data_href
            play_html = requests.get(url)
            music_soup = BeautifulSoup(play_html.text, features="html.parser")
            author = None
            title = None
            music_url = None

            for script in music_soup.select("script"):
                script = str(script)
                if script.find("music") >= 0:
                    lines = script.split("\n")
                    for line in lines:
                        line = line.strip()
                        if line.split(":")[0] == "author":
                            author = line.split(":")[1].strip().strip(',')
                        elif line.split(":")[0] == "title":
                            title = line.split(":")[1].strip().strip(',')
                        elif line.split(":")[0] == "url":
                            music_url = line[len("url:"):].strip().strip(",")

            if author is not None and title is not None and music_url is not None:
                author = author.strip("'")
                title = title.strip("'")
                music_url = music_url.strip("'")
                download_url = domain + music_url

                response = requests.get(download_url)
                '''while response.status_code is None or response.status_code != 200:
                    response = requests.get(download_url)
                    #logging.info("request play page failed, code=%d" % response.status_code)
                    #time.sleep(1)
                '''
                if response.headers["Content-Type"] == "application/json;charset=UTF-8":
                    res_json = json.loads(response.text)
                    if res_json["code"] == -460:
                        logging.info("request play page failed, msg=%s, try later..." % res_json["message"])
                        continue
                elif response.status_code == 200:
                    suffix = response.headers["Content-Type"]
                    if suffix.find("/") > 0:
                        suffix = suffix.split("/")[1]
                    save_path = "%s/%s - %s.%s" % (SAVE_PATH, title, author, suffix)
                    with open(save_path, "wb") as fp:
                        fp.write(response.content)
                        logging.info("download success, saved as %s" % save_path)
                    if suffix.upper() != "MP3":
                        mp3_path = "%s/%s - %s.mp3" % (SAVE_PATH, title, author)
                        ff = FFmpeg(inputs={save_path: None}, outputs={mp3_path: None}, global_options="-y")
                        ff.run()
                        os.remove(save_path)


if __name__ == "__main__":
    main()

