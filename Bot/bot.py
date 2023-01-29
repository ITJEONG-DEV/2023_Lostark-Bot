import datetime
import time

import pymysql
import twitter

from util import read_json
from adventure_island import get_adventure_island


class TwitterBot:
    def __init__(self):
        self.data = read_json("./data/key.json")

        print(self.data)

        self.auth = None
        self.api = None

        self.con = None

    def start(self):
        self.api = twitter.Api(
            consumer_key=self.data["api_key"],
            consumer_secret=self.data["api_key_secret"],
            access_token_key=self.data["access_token"],
            access_token_secret=self.data["access_token_secret"]
        )

        self.con = pymysql.connect(host='localhost', user='root', password='September 19th, 2022 q!w@e#r$5678',
                                   db='LOA', charset='utf8')

        datetime.timezone(datetime.timedelta(seconds=32400))

    def run(self):
        message = [
            "\n".join([" 월요일 컨텐츠>", "- 카오스 게이트", "- 모험섬"]),
            "\n".join([" 화요일 컨텐츠>", "- 필드보스", "- 유령선", "- 모험섬"]),
            "\n".join([" 로요일 컨텐츠>", "- 모험섬", "- 툴루비크 전장"]),
            "\n".join([" 목요일 컨텐츠>", "- 카오스 게이트", "- 유령선", "모험섬"]),
            "\n".join([" 금요일 컨텐츠>", "- 필드보스", "- 모험섬"]),
            "\n".join([" 토요일 컨텐츠>", "- 카오스 게이트", "- 유령선", "- 모험섬(오전/오후)", "     "
                                                                          ""
                                                                          ""
                                                                          ""
                                                                          "- 툴루비크 전장"]),
            "\n".join([" 일요일 컨텐츠>", "- 카오스 게이트", "- 필드보스", "- 모험섬(오전/오후)", "- 툴루비크 전장"]),
        ]
        while True:
            time.sleep(1)

            now = datetime.datetime.now()
            day = now.weekday()

            # 주말 모험섬 공지 - 07:00
            if day == 5 or day == 6:
                if now.hour == 7 and now.minute == 0 and now.second == 0:
                    cur = self.con.cursor()
                    sql = f"SELECT `ISLAND`, `REWARD` FROM ADVENTURE_ISLAND WHERE `ID` = {now.strftime('%Y%m%d')};"
                    cur.execute(sql)
                    rows = cur.fetchall()

                    island = rows[0][0].split(',')
                    reward = rows[0][1].split(',')

                    link = get_adventure_island(island, reward, True)
                    self.post_image(link, now.strftime("%Y-%m-%d") + message[day] + "\n등장하는 모험섬 정보>")

            # 평일 모험섬 공지 - 09:00
            else:
                if now.hour == 9 and now.minute == 9 and now.second == 0:
                    cur = self.con.cursor()
                    sql = f"SELECT `ISLAND`, `REWARD` FROM ADVENTURE_ISLAND WHERE `ID` = {now.strftime('%Y%m%d')};"
                    cur.execute(sql)
                    rows = cur.fetchall()

                    island = rows[0][0].split(',')
                    reward = rows[0][1].split(',')

                    link = get_adventure_island(island, reward, False)
                    self.post_image(link, now.strftime("%Y-%m-%d") + message[day] + "\n등장하는 모험섬 정보>")

    def test(self):
        if self.api is None:
            self.start()

        # account = "@conie_zoa"
        # statuses = self.api.GetUserTimeline(screen_name=account, count=10)
        # print(statuses)

        # self.api.update_status("test")

    def post_image(self, image_path, message):
        media = self.api.media_upload(image_path)

        self.api.update_status(status=message, media_ids=[media.media_id])
