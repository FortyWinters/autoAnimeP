import sys
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from exts import db
from common import *
from logManager import m_LogManager

logger = m_LogManager.getLogObj(sys.argv[0])


class AnimeList(db.Model):
    __tablename__ = "anime_list"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    anime_name = db.Column(db.String(40), nullable=True, unique=True)
    mikan_id = db.Column(db.Integer, nullable=True, unique=True)
    update_day = db.Column(db.Integer, nullable=True, comment='剧场版和ova为0')
    img_url = db.Column(db.String(40), nullable=False)
    anime_type = db.Column(db.Integer, nullable=True, comment='0为番剧,1为剧场版,2为ova')
    subscribe_status = db.Column(db.Integer, nullable=True, comment='0为未订阅,1为已订阅')


class AnimeSeed(db.Model):
    __tablename__ = "anime_seed"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mikan_id = db.Column(db.Integer, nullable=False)
    subgroup_id = db.Column(db.Integer, nullable=False)
    episode = db.Column(db.Integer, nullable=False)
    seed_name = db.Column(db.String(200), nullable=False)
    seed_url = db.Column(db.String(200), nullable=False, unique=True)


class AnimeTask(db.Model):
    __tablename__ = "anime_task"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 任务的默认id
    anime_id = db.Column(db.Integer, nullable=False, unique=True)
    # 剧集对应的番名（AnimeList）的id
    status = db.Column(db.Integer)
    # 下载的状态 0表示还没有开始下载 1表示下载成功 2表示下载开始但是过程失败
    episode = db.Column(db.String(40))
    # 剧集名称


# TODO 继续优化 @bjrbh
def insert_data_to_anime_list(anime_name, mikan_id, img_url, update_day, anime_type, subscribe_status):
    try:
        anime_list = AnimeList(anime_name=anime_name, mikan_id=mikan_id, img_url=img_url, update_day=update_day,
                               anime_type=anime_type, subscribe_status=subscribe_status)
        db.session.add_all([anime_list])
        db.session.commit()
    except Exception as e:
        print("[ERROR][MODELS]insert_data_to_anime_list failed, " +
              "anime_name: {}, mikan_id: {}, img_url: {}, update_day: {}, anime_type: {}, subscribe_status: {}".format(
                  anime_name, mikan_id, img_url, update_day, anime_type, subscribe_status))
        return False
    else:
        return True


# ----------------[更新]👆使用session_commit用于数据库回滚 均是可选字段
def insert_data_to_anime_list_new(mikan_id, anime_name="", img_url="", update_day="0", anime_type="0",
                                  subscribe_status="0"):
    anime_list = AnimeList(anime_name=anime_name, mikan_id=mikan_id, img_url=img_url, update_day=update_day,
                           anime_type=anime_type, subscribe_status=subscribe_status)
    db.session.add_all([anime_list])
    return session_commit()


# TODO 继续优化 @bjrbh
def insert_data_to_anime_seed(mikan_id, episode, seed_url, subgroup_id, seed_name):
    try:
        anime_seed = AnimeSeed(mikan_id=mikan_id, episode=episode, seed_url=seed_url, subgroup_id=subgroup_id,
                               seed_name=seed_name)
        db.session.add_all([anime_seed])
        db.session.commit()
    except Exception as e:
        print("[ERROR][MODELS]insert_data_to_anime_seed failed, " +
              "mikan_id: {}, episode: {}, seed_url: {}, subgroup_id: {}, seed_name: {}".format(
                  mikan_id, episode, seed_url, subgroup_id, seed_name))
        return False
    else:
        return True


# ----------------[更新]👆使用session_commit用于数据库回滚
def insert_data_to_anime_seed_new(mikan_id, episode, seed_url, subgroup_id, seed_name):
    anime_seed = AnimeSeed(mikan_id=mikan_id, episode=episode, seed_url=seed_url, subgroup_id=subgroup_id,
                           seed_name=seed_name)
    db.session.add_all([anime_seed])
    return session_commit()


# TODO 继续优化 @bjrbh
# 初步查询语句 可以修改输入参数
def query_list_by_anime_name():  # 增加过滤条件进行查询
    result = db.session.query(AnimeList).all()
    list = []
    for data in result:
        cur = Anime(data.anime_name, data.mikan_id, data.img_url, data.update_day, data.anime_type,
                    data.subscribe_status)
        # list.append(cur)
        dic = {
            "id": data.index,
            "anime_name": data.anime_name,
            "mikan_id": data.mikan_id,
            "img_url": data.img_url,
            "update_day": data.update_day,
            "anime_type": data.anime_type,
            "subscribe_status": data.subscribe_status
        }
        list.append(dic)

    return list


# ----------------[更新]👆使用可选参数用于条件查询
def query_list_by_anime_name_new(anime_name='', mikan_id=-1, img_url='', update_day=-1, anime_type=-1,
                                 subscribe_status=-1):  # 增加过滤条件进行查询
    session = db.session.query(AnimeList)
    if anime_name != '':
        session = session.filter_by(anime_name=anime_name)
    if mikan_id != -1:
        session = session.filter_by(mikan_id=mikan_id)
    if update_day != -1:
        session = session.filter_by(update_day=update_day)
    if anime_type != -1:
        session = session.filter_by(anime_type=anime_type)
    if subscribe_status != -1:
        session = session.filter_by(subscribe_status=subscribe_status)
    result = session.all()
    list = []
    for data in result:
        cur = Anime(data.anime_name, data.mikan_id, data.img_url, data.update_day, data.anime_type,
                    data.subscribe_status)
        # list.append(cur)
        dic = {
            "id": data.index,
            "anime_name": data.anime_name,
            "mikan_id": data.mikan_id,
            "img_url": data.img_url,
            "update_day": data.update_day,
            "anime_type": data.anime_type,
            "subscribe_status": data.subscribe_status
        }
        list.append(dic)

    return list


# TODO 继续优化 @bjrbh
def query_seed_by_anime_name(mikan_id):  # 增加过滤条件进行查询
    result = db.session.query(AnimeSeed).filter(AnimeSeed.mikan_id == mikan_id).all()
    list = []
    for data in result:
        cur = Seed(data.mikan_id, data.episode, data.seed_url, data.subgroup_id, data.seed_name)
        # list.append(cur)
        dic = {
            "id": data.index,
            "mikan_id": data.mikan_id,
            "episode": data.episode,
            "seed_url": data.seed_url,
            "subgroup_id": data.subgroup_id,
            "seed_name": data.seed_name
        }
        list.append(dic)

    return list


def update_list_subscribe_status(mikan_id, subscribe_status):
    db.session.query(AnimeList).filter_by(mikan_id=mikan_id).update({"subscribe_status": subscribe_status})
    db.session.commit()


# delete anime_list

def delete_anime_list_by_condition(anime_name='', mikan_id=-1, update_day=-1, anime_type=-1, subscribe_status=-1):
    session = db.session.query(AnimeList)
    if anime_name != '':
        session = session.filter_by(anime_name=anime_name)
    if mikan_id != -1:
        session = session.filter_by(mikan_id=mikan_id)
    if update_day != -1:
        session = session.filter_by(update_day=update_day)
    if anime_type != -1:
        session = session.filter_by(anime_type=anime_type)
    if subscribe_status != -1:
        session = session.filter_by(subscribe_status=subscribe_status)
    query = session.all()
    count = 0
    for data in query:
        db.session.delete(data)
        count = count + 1
    if count > 0:
        return session_commit()
    return False


# from sqlalchemy.exc import SQLAlchemyError
# from flask import current_app


# class DbSessionCommit():
#     @staticmethod
#     def add(self):
#         db.session.add(self)
#         return session_commit()

#     @staticmethod
#     def update(self):
#         return session_commit()

#     @staticmethod
#     def delete(self):
#         db.session.delete(self)
#         return session_commit()

# class User(db.Model, DbSessionCommit):
#     __tablename__ = 't_user'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)

def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        logger.warning('[Models]Exception :' + reason)
        return False
    else:
        return True
