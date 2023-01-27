import datetime
from PIL import Image


# island = [ "하모니 섬", "죽음의 협곡", "고요한 안식의 섬" ]
# reward = [ "카드", "실링", "골드" ]
def get_adventure_island(island, reward):
    image = Image.new('RGB', (460 * 3, 290 + 260), (17, 18, 20))
    for i in range(3):
        island_image = Image.open(f'data/island/{island[i]}.jpg')
        island_image = island_image.resize((460, 290))

        reward_image = Image.open(f'data/reward/{reward[i]}.jpg')
        reward_image = reward_image.resize((460, 260))

        new_image = Image.new('RGB', (460, 290 + 260))
        new_image.paste(island_image, (0, 0))
        new_image.paste(reward_image, (0, 290))

        image.paste(new_image, (460 * i, 0))

    now = datetime.datetime.now()
    image.save(f'data/today/{now.strftime("%Y%M%d")}.jpg')

    return image


if __name__ == "__main__":
    image = get_adventure_island(
        island=["하모니 섬", "죽음의 협곡", "고요한 안식의 섬"],
        reward=["카드", "실링", "골드"]
    )

    image.show()
