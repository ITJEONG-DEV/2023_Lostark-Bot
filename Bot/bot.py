import twitter
from util import read_json


class TwitterBot:
    def __init__(self):
        self.data = read_json("./data/key.json")

        print(self.data)

        self.auth = None
        self.api = None

    def start(self):
        self.api = twitter.Api(
            consumer_key=self.data["api_key"],
            consumer_secret=self.data["api_key_secret"],
            access_token_key=self.data["access_token"],
            access_token_secret=self.data["access_token_secret"]
        )

    def test(self):
        if self.api is None:
            self.start()

        account = "@conie_zoa"
        statuses = self.api.GetUserTimeline(screen_name=account, count=10)
        print(statuses)

        # self.api.update_status("test")
