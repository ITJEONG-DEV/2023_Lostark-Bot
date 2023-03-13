import datetime
from PIL import Image, ImageDraw, ImageFont

import os


# island = [ "하모니 섬", "죽음의 협곡", "고요한 안식의 섬" ]
# reward = [ "카드", "실링", "골드" ]
def get_adventure_island(island, reward, double=False):
    title_size = (460 * 3, 120)
    island_size = (460, 290)
    reward_size = (460, 260)
    content_size = (460, 290 + 260)

    now = datetime.datetime.now()
    font = ImageFont.truetype("C:/USERS/DEV2/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/NANUMBARUNGOTHICBOLD.TTF", size=16)
    background_color = (0, 0, 0)
    font_color = (255, 255, 255)

    if double:
        width = title_size[0]
        height = (title_size[1] + island_size[1] + reward_size[1]) * 2

        image = Image.new('RGB', (width, height), background_color)

        for j in range(2):
            # paste content
            for i in range(3):
                island_image = Image.open(f'data/island/{island[i + j * 3]}.jpg')
                island_image = island_image.resize(island_size)

                reward_image = Image.open(f'data/reward/{reward[i + j * 3]}.jpg')
                reward_image = reward_image.resize(reward_size)

                new_image = Image.new('RGB', content_size)
                new_image.paste(island_image, (0, 0))
                new_image.paste(reward_image, (0, 290))

                image.paste(new_image, (460 * i, title_size[1] + int(height / 2 * j)))

            # add title
            drawable_image = ImageDraw.Draw(image)
            title = now.strftime("%Y-%m-%d") + " 모험섬"
            if j == 0:
                title += " 오전 타임 (09:00/11:00/13:00)"
            elif j == 1:
                title += " 오후 타임 (19:00/21:00/23:00)"

            w, h = drawable_image.textsize(title, font=font)
            x, y = (title_size[0] - w) / 2, (title_size[1] + height * j - h) / 2
            drawable_image.text((x, y), title, fill=font_color, font=font)

    else:
        width = title_size[0]
        height = (title_size[1] + island_size[1] + reward_size[1])

        image = Image.new('RGBA', (width, height), background_color)

        # paste content
        for i in range(3):
            island_image = Image.open(f'adventure_island/data/island/{island[i]}.jpg')
            island_image = island_image.resize(island_size)

            reward_image = Image.open(f'adventure_island/data/reward/{reward[i]}.jpg')
            reward_image = reward_image.resize(reward_size)

            new_image = Image.new('RGB', content_size)
            new_image.paste(island_image, (0, 0))
            new_image.paste(reward_image, (0, 290))

            image.paste(new_image, (460 * i, title_size[1]))

        # add title
        drawable_image = ImageDraw.Draw(image)
        title = now.strftime("%Y-%m-%d") + " 모험섬 (11:00/13:00/19:00/21:00/23:00)"
        w, h = drawable_image.textsize(title, font=font)
        x, y = (title_size[0] - w) / 2, (title_size[1] - h) / 2
        drawable_image.text((x, y), title, fill=font_color, font=font)

    link = f'adventure_island/data/today/{now.strftime("%Y%m%d")}.jpg'
    image.save(link)

    # return image
    return link


# 파일이 있는지 확인하고, 없다면 다운로드 받아서 반환
def get_image(dir: str, name: str):
    if not os.path.isfile(f'{dir}/{name}.png'):
        print("download request")

    return Image.open(f'{dir}/{name}.png').convert("RGBA")

# 일반 고급 희귀 영웅 전설 유물 고대 에스더
# 회색 초록 파랑 보라 금색 빨강 하양 하늘색
grade_color = {
    "일반": (78, 80, 77),
    "고급": (56, 74, 34),
    "희귀": (15, 49, 74),
    "영웅": (65, 28, 79),
    "전설": (115, 78, 25),
    "유물": (164, 69, 15),
    "고대": (248, 228, 178),
    "에스더": (122, 245, 247)
}


def get_item_color(grade: str):
    if grade in grade_color.keys():
        return grade_color[grade]
    else:
        return grade_color["일반"]


window_size = (1024, 512)
icon_size = (64, 64)
title_font = ImageFont.truetype("C:/USERS/DEV2/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/NANUMBARUNGOTHICBOLD.TTF", size=40)
time_font = ImageFont.truetype("C:/USERS/DEV2/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/NANUMBARUNGOTHIC.TTF", size=32)
island_font = ImageFont.truetype("C:/USERS/DEV2/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/NANUMBARUNGOTHIC.TTF", size=28)
item_color = (50, 50, 50)

background_color = (0, 0, 0)
title_back_color = (32, 32, 32)

# background_color = (32, 32, 32)
# title_back_color = (0, 0, 0)

font_color = (255, 255, 255)
title_color = (255, 210, 40)
icon_gap = 4  # 아이콘 사이의 공백
content_gap = 32  # 컨텐츠 사이의 공백
max_reward_num = 8
margin = 4


def make_rewards_box(rewards: [], grades: []):
    width, height = icon_size[0] * len(rewards) + icon_gap * (len(rewards) - 1), icon_size[1]
    reward_box_size = (width, height)
    reward_box = Image.new('RGBA', reward_box_size, background_color)

    for i in range(len(rewards)):
        reward = rewards[i]
        grade = grades[i]

        reward_back = Image.new('RGBA', icon_size, get_item_color(grade))

        reward_image = get_image(f'data/reward', reward)
        reward_image = reward_image.resize(icon_size)

        start_x, start_y = (icon_size[0] + icon_gap) * i, 0
        reward_image = Image.alpha_composite(reward_back, reward_image)
        reward_box.paste(reward_image, (start_x, start_y), reward_image)

    return reward_box


def make_island_box(island: str, rewards: [], grades: []):
    width, height = 1024 - icon_size[0] * 2 + margin * 2, icon_size[1] + margin * 2
    island_box = Image.new('RGBA', (width, height), background_color)

    # island
    island_image = get_image(f'data/island', island)
    island_image = island_image.resize(icon_size)

    island_box.paste(island_image, (margin, margin), island_image)

    # text
    drawable_image = ImageDraw.Draw(island_box)
    w, h = drawable_image.textsize(island, font=island_font)
    x, y = icon_size[0] + icon_gap * 4 + margin, (height - h) / 2
    drawable_image.text((x, y), island, fill=font_color, font=island_font)

    # reward
    rewards_box = make_rewards_box(rewards, grades)
    start_x, start_y = width - icon_size[0] * len(rewards) - icon_gap * (len(rewards) - 1) - margin, margin
    island_box.paste(rewards_box, (start_x, start_y), rewards_box)

    return island_box


def make_island_boxes(island_rewards_infoes: [[]]):
    width, height = 1024 - icon_size[0] * 2 + margin * 2, icon_size[1] * 3 + content_gap * 2 + margin * 6
    island_boxes = Image.new('RGBA', (width, height))

    for i in range(len(island_rewards_infoes)):
        item = island_rewards_infoes[i]

        island_box = make_island_box(item[0], item[1], item[2])
        start_x, start_y = 0, (icon_size[1] + content_gap) * i
        island_boxes.paste(island_box, (start_x, start_y), island_box)

    return island_boxes


def make_island_content(island_rewards_infoes: [[]], time_text):
    width, height = 1024 - icon_size[0] * 2 + margin * 2, icon_size[1] * 3 + content_gap * 2 + icon_size[1] * 2 + margin * 6
    island_content = Image.new('RGBA', (width, height))

    # text
    drawable_image = ImageDraw.Draw(island_content)
    w, h = drawable_image.textsize(time_text, font=time_font)
    x, y = (width - w) / 2, h / 2
    drawable_image.text((x, y), time_text, fill=font_color, font=time_font)

    # image
    island_boxes = make_island_boxes(island_rewards_infoes)
    start_x, start_y = 0, icon_size[1] + content_gap
    island_content.paste(island_boxes, (start_x, start_y), island_boxes)

    return island_content


def make_daily_adventure_island(island_rewards_infoes: [[]], date_text):
    daily_adventure_island = None

    if len(island_rewards_infoes) == 6:
        daily_adventure_island_content = Image.new('RGBA', (window_size[0], window_size[1] * 2), title_back_color)

        # title
        drawable_image = ImageDraw.Draw(daily_adventure_island_content)
        w, h = drawable_image.textsize(date_text, font=title_font)
        x, y = (window_size[0] - w) / 2, h
        drawable_image.text((x, y), date_text, fill=title_color, font=title_font)

        island_content_1 = make_island_content(island_rewards_infoes[:3], "09:00/11:00/13:00")
        start_x, start_y = icon_size[0] - margin, icon_size[1] + content_gap
        daily_adventure_island_content.paste(island_content_1, (start_x, start_y), island_content_1)

        island_content_2 = make_island_content(island_rewards_infoes[3:], "19:00/21:00/23:00")
        start_x, start_y = icon_size[0] - margin, icon_size[1] * 7 + content_gap * 4
        daily_adventure_island_content.paste(island_content_2, (start_x, start_y), island_content_2)

    else:
        daily_adventure_island_content = Image.new('RGBA', window_size, title_back_color)

        # title
        drawable_image = ImageDraw.Draw(daily_adventure_island_content)
        w, h = drawable_image.textsize(date_text, font=title_font)
        x, y = (window_size[0] - w) / 2, h
        drawable_image.text((x, y), date_text, fill=title_color, font=title_font)

        island_content = make_island_content(island_rewards_infoes, "11:00/13:00/19:00/21:00/23:00")
        start_x, start_y = icon_size[0] - margin, icon_size[1] + content_gap
        daily_adventure_island_content.paste(island_content, (start_x, start_y), island_content)

    return daily_adventure_island_content


if __name__ == "__main__":
    # image = get_adventure_island(
    #     island=["하모니 섬", "죽음의 협곡", "고요한 안식의 섬", "하모니 섬", "죽음의 협곡", "고요한 안식의 섬"],
    #     reward=["카드", "실링", "골드", "카드", "실링", "골드"],
    #     double=False
    # )

    # image.show()
    make_daily_adventure_island([
        ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "실링"], ["전설", "고급", "희귀", "일반"]],
        ["기회의 섬", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "고급", "희귀", "일반", "일반"]],
        ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "고급", "희귀", "일반", "일반"]]
    ], "2023-03-11 모험섬 일정") \
    .save("D:/평일_테스트1.png")
    #.show()

    make_daily_adventure_island([
        ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "실링"], ["전설", "고급", "희귀", "일반"]],
        ["기회의 섬", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "고급", "희귀", "일반", "일반"]],
        ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "고급", "희귀", "일반", "일반"]],
        ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "실링"], ["전설", "고급", "희귀", "일반"]],
        ["기회의 섬", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "고급", "희귀", "일반", "일반"]],
        ["스노우팡 아일랜드", ["전설 ~ 고급 카드 팩", "영혼의 잎사귀", "인연의 돌", "해적 주화", "실링"], ["전설", "영웅", "희귀", "고급", "일반"]],
    ], "2023-03-11 모험섬 일정") \
    .save("D:/주말_테스트1.png")
    #.show()
