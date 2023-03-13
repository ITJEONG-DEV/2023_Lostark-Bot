import os

import pymysql

from util import read_json

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
key = read_json(path + "/data/key.json")


def connect():
    mysql = key["mysql"]
    return pymysql.connect(host=mysql["host"], user=mysql["user"], password=mysql["password"],
                           db=mysql["db"], charset='utf8')


con = connect()


# 기본 모험섬 정보가 DB에 있는지 확인
def check_adventure_island_available(name):
    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()
    sql = f"SELECT COUNT(`ISLAND_NAME`) AS `COUNT` FROM `ISLAND_CONST` WHERE `ISLAND_NAME`='{name}';"
    cur.execute(sql)
    result = cur.fetchall()

    if result[0][0] == 0:
        return False
    else:
        return True


# 아이템 정보가 DB에 있는지 확인
def check_reward_item_available(name):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in name:
            return True

    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()
    sql = f"SELECT COUNT(`REWARD_NAME`) AS `COUNT` FROM `REWARD_ITEM` WHERE `REWARD_NAME`='{name}';"
    cur.execute(sql)
    result = cur.fetchall()

    if result[0][0] == 0:
        return False
    else:
        return True


# 기본 리워드 정보가 DB에 있는지 확인
def check_reward_item_const_available(island, reward):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in reward:
            return True

    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()
    sql = f"SELECT COUNT(`REWARD_NAME_`) AS `COUNT` FROM `ISLAND_REWARD_CONST` WHERE `REWARD_NAME_`='{reward}' AND `ISLAND_NAME_`='{island}';"
    cur.execute(sql)
    result = cur.fetchall()

    if result[0][0] == 0:
        return False
    else:
        return True


# 모험섬 스케쥴이 DB에 있는지 확인
def check_island_reward_schedule_available(date, time, island, reward):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in reward:
            return True

    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()
    sql = f"SELECT COUNT(`REWARD_NAME`) AS `COUNT` FROM `ISLAND_REWARD_SCHEDULE` WHERE `REWARD_NAME`='{reward}' AND `ISLAND_NAME`='{island}' AND `APPEAR_DATE`='{date}' AND `PART_TIME`='{time}';"
    cur.execute(sql)
    result = cur.fetchall()

    if result[0][0] == 0:
        return False
    else:
        return True


# 모험섬 보상 스케쥴이 DB에 있는지 확인
def check_island_schedule_available(date, time, name):
    global con
    if not con.begin():
        con = connect()

    cur = con.cursor()
    sql = f"SELECT COUNT(`ISLAND_NAME`) AS `COUNT` FROM `ISLAND_SCHEDULE` WHERE `ISLAND_NAME`='{name}' AND `APPEAR_DATE`='{date}' AND `PART_TIME`='{time}';"
    cur.execute(sql)
    result = cur.fetchall()

    if result[0][0] == 0:
        return False
    else:
        return True


# 기본 모험섬 정보를 DB에 추가
def add_adventure_island_const(name, url):
    global con
    if not con.begin():
        con = connect()

    try:
        cur = con.cursor()
        sql = f"INSERT INTO `ISLAND_CONST`(`ISLAND_NAME`, `ISLAND_ICON`) VALUES ('{name}', '{url}');"
        cur.execute(sql)
        con.commit()

    except Exception as e:
        print(e)


# 아이템 정보를 DB에 추가
def add_reward_item_const(name, url, grade):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in name:
            return

    global con
    if not con.begin():
        con = connect()

    try:
        cur = con.cursor()
        sql = f"INSERT INTO `REWARD_ITEM`(`REWARD_NAME`, `REWARD_ICON`, `ITEM_GRADE`) VALUES ('{name}', '{url}', '{grade}');"
        cur.execute(sql)
        con.commit()

    except Exception as e:
        print(e)


# 기본 리워드 정보를 DB에 추가
def add_default_reward_item(island, reward):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in reward:
            return

    global con
    if not con.begin():
        con = connect()

    try:
        cur = con.cursor()
        sql = f"INSERT INTO `ISLAND_REWARD_CONST`(`ISLAND_NAME_`, `REWARD_NAME_`) VALUES ('{island}', '{reward}');"
        cur.execute(sql)
        con.commit()

    except Exception as e:
        print(e)


# 모험섬 출연 정보를 DB에 추가
def add_adventure_island_schedule(name, date, time):
    global con
    if not con.begin():
        con = connect()
    try:
        cur = con.cursor()
        sql = f"INSERT INTO `ISLAND_SCHEDULE`(`APPEAR_DATE`, `PART_TIME`, `ISLAND_NAME`) VALUES ('{date}', '{time}', '{name}');"
        cur.execute(sql)
        con.commit()

    except Exception as e:
        print(e)


# 모험섬 보상 스케쥴을 DB에 추가
def add_island_reward_schedule(date, time, island, reward):
    except_keyword_list = key["lostark"]["except_item"]

    for keyword in except_keyword_list:
        if keyword in reward:
            return

    global con
    if not con.begin():
        con = connect()

    try:
        cur = con.cursor()
        sql = f"INSERT INTO `ISLAND_REWARD_SCHEDULE`(`APPEAR_DATE`, `PART_TIME`, `ISLAND_NAME`, `REWARD_NAME`) VALUES ('{date}', '{time}', '{island}', '{reward}');"
        cur.execute(sql)
        con.commit()

    except Exception as e:
        print(e)


if __name__ == "__main__":
    print("hi")
    print(check_reward_item_const_available(island="기회의 섬", reward="실링"))

    # result = check_reward_item_available("스노우팡 아일랜드 섬의 마음")
    # print(result)
    #
    # result = check_reward_item_available("골드")
    # print(result)
    #
    # result = add_reward_item_const("골드", "https://cdn-lostark.game.onstove.com/EFUI_IconAtlas/Money/Money_4.png")
    #
    # result = check_reward_item_available("골드")
    # print(result)

    #
    # result = add_adventure_island_const("스노우팡 아일랜드",
    #                                     "https://cdn-lostark.game.onstove.com/EFUI_IconAtlas/Island_Icon/Island_Icon_98.png")
    # print(result)
    #
    # result = check_adventure_island_available("스노우팡 아일랜드")
    # print(result)

    # result = add_adventure_island_schedule('스노우팡 아일랜드', '2203-03-11', '0');
    # print(result)
