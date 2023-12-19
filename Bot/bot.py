import datetime
import time
import os

import pymysql
import tweepy

from util import read_json
from adventure_island import parse_adventure_island, get_adventure_island
from challenge_contents import get_weekly_challenge_contents


class TwitterBot:
    def __init__(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        self.data = read_json(path + "/data/key.json")["twitter"]
        self.lostark = read_json(path + "/data/key.json")["lostark"]

        self.auth = None
        self.api = None

        self.con = None

    def start(self):
        auth = tweepy.OAuthHandler(
            consumer_key=self.data["api_key"],
            consumer_secret=self.data["api_key_secret"]
        )

        auth.set_access_token(
            key=self.data["access_token"],
            secret=self.data["access_token_secret"]
        )

        self.api = tweepy.API(auth)

        datetime.timezone(datetime.timedelta(seconds=32400))

    def filter_data(auth):
        data = get_island_info(auth)

        today_island = []

        today = datetime.datetime.now().strftime("%Y-%m-%d")

        for island in data:
            start_times = island["StartTimes"]

            if start_times is None:
                continue

            # 오늘의 모험섬인지 확인
            for start_time in start_times:
                words = start_time.split("T")
                if words[0] == today:
                    today_island.append({
                        "name": island["ContentsName"],
                        "icon": island["ContentsIcon"],
                        "time": words[1].split(":")[0]  ## hour
                    })
                    break

            # 오늘의 모험섬 보상인지 확인
            reward_items = island["RewardItems"]

            if reward_items is None:
                continue

            for reward_item in reward_items:
                # 공통 보상 제외
                ignore_item = ["인연의 돌"]
                if reward_item["Name"] in ignore_item:
                    continue

                # 기본 보상 제외
                if reward_item["StartTimes"] is not None:
                    exception = False
                    exception_reward = ["비밀지도", "모험물", "수호", "풍요"]

                    for reward in exception_reward:
                        if reward in reward_item["Name"]:
                            exception = True

                    if exception:
                        if "reward" not in today_island[len(today_island) - 1].keys():
                            today_island[len(today_island) - 1]["reward"] = []

                        today_island[len(today_island) - 1]["reward"].append({
                            "name": reward_item["Name"],
                            "icon": reward_item["Icon"],
                            "grade": reward_item["Grade"]
                        })

                if reward_item["StartTimes"] is not None:
                    start_times = reward_item["StartTimes"]

                    for start_time in start_times:
                        words = start_time.split("T")
                        if words[0] == today:
                            if "reward" not in today_island[len(today_island) - 1].keys():
                                today_island[len(today_island) - 1]["reward"] = []

                            today_island[len(today_island) - 1]["reward"].append({
                                "name": reward_item["Name"],
                                "icon": reward_item["Icon"],
                                "grade": reward_item["Grade"]
                            })
                            break

        return today_island

    def get_adventure_island_information(self, key):
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        link = f'./result/today/{date}.png'

        if not os.path.isfile(link):
            island_info = filter_data(auth)

            image = make_daily_adventure_island(island_info, f"{date} 모험섬 일정")
            # link = f'./adventure_island/data/today/{date}.png'
            # link = f'D:/{date}.png'
            image.save(link)

        return link

    def run(self):
        message = [
            "\n".join([" 월요일 컨텐츠>", "- 카오스 게이트", "- 모험섬"]),
            "\n".join([" 화요일 컨텐츠>", "- 필드보스", "- 유령선", "- 모험섬"]),
            "\n".join([" 로요일 컨텐츠>", "- 모험섬", "- 툴루비크 전장"]),
            "\n".join([" 목요일 컨텐츠>", "- 카오스 게이트", "- 유령선", "- 모험섬"]),
            "\n".join([" 금요일 컨텐츠>", "- 필드보스", "- 모험섬"]),
            "\n".join([" 토요일 컨텐츠>", "- 카오스 게이트", "- 유령선", "- 모험섬(오전/오후)", "- 툴루비크 전장"]),
            "\n".join([" 일요일 컨텐츠>", "- 카오스 게이트", "- 필드보스", "- 모험섬(오전/오후)", "- 툴루비크 전장"]),
        ]
        while True:
            time.sleep(1)

            now = datetime.datetime.now()
            day = now.weekday()

            if now.hour == 8 and now.minute == 0 and now.second == 0:
                parse_adventure_island(authorization=f"Bearer {self.lostark['api_key']}")
                link = get_adventure_island(now.strftime('%Y-%m-%d'), day >= 5)
                status = self.post_image(link, now.strftime("%Y-%m-%d") + message[day] + "\n\n등장하는 모험섬 정보>")

                if day == 2:
                    link = get_weekly_challenge_contents(authorization=f"Bearer {self.lostark['api_key']}")
                    self.post_image(link, "주간 도전 컨텐츠 안내>", reply_id=status["id_str"])

    def test(self):
        if self.api is None:
            self.start()

        message = [
            "\n".join([" 월요일 컨텐츠>", "- 카오스 게이트", "- 모험섬"]),
            "\n".join([" 화요일 컨텐츠>", "- 필드보스", "- 유령선", "- 모험섬"]),
            "\n".join([" 로요일 컨텐츠>", "- 모험섬", "- 툴루비크 전장"]),
            "\n".join([" 목요일 컨텐츠>", "- 카오스 게이트", "- 유령선", "- 모험섬"]),
            "\n".join([" 금요일 컨텐츠>", "- 필드보스", "- 모험섬"]),
            "\n".join([" 토요일 컨텐츠>", "- 카오스 게이트", "- 유령선", "- 모험섬(오전/오후)", "- 툴루비크 전장"]),
            "\n".join([" 일요일 컨텐츠>", "- 카오스 게이트", "- 필드보스", "- 모험섬(오전/오후)", "- 툴루비크 전장"]),
        ]

        time.sleep(1)

        now = datetime.datetime.now()
        day = now.weekday()

        parse_adventure_island(authorization=f"Bearer {self.lostark['api_key']}")
        link = get_adventure_island(now.strftime('%Y-%m-%d'), day >= 5)
        status = self.post_image(link, now.strftime("%Y-%m-%d") + message[day] + "\n\n등장하는 모험섬 정보>")

        print(status)

        # link = get_weekly_challenge_contents(authorization=f"Bearer {self.lostark['api_key']}")
        # self.post_image(link, "주간 도전 컨텐츠 안내>", reply_id=status.id_str)

        print("탈출")

    def challenge_contents_test(self):
        link = get_weekly_challenge_contents(authorization=f"Bearer {self.lostark['api_key']}")
        # self.post_image(link, "주간 도전 컨텐츠 안내>")


    def post_image(self, image_path, message, reply_id=None):
        media = self.api.media_upload(image_path)

        status = self.api.update_status(status=message, media_ids=[media.media_id], in_reply_to_status_id=reply_id)
        print(f"다음의 내용을 트윗합니다.\n{message}, {media.media_id}")

        return status
