from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from config import pstgr


engine = create_engine(
    'postgresql://{}:{}@localhost/elsewhere'.format(
        pstgr['login'], pstgr['pass']), echo=True)
Base = declarative_base()


class UserEntity(Base):
    __tablename__ = 'userentities'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password = Column(String)
    username = Column(String)
    email = Column(String)


class City(Base):
    __tablename__ = 'vkcities'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    vkfriends = relationship("VKFriend", back_populates="city")


class VKFriend(Base):
    __tablename__ = 'vkfriends'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    vk_id = Column(Integer)
    last_name = Column(String)
    sex = Column(Integer)
    nickname = Column(String)
    domain = Column(String)
    bdate = Column(String)
    city_id = Column(Integer, ForeignKey('vkcities.id'))
    city = relationship("City", back_populates="vkfriends")

    def __repr__(self):
        return ("Person("
                "first_name='{}',"
                "vk_id={},"
                "last_name='{}',"
                "sex={},"
                "nickname='{}',"
                "domain='{}',"
                "bdate='{}')").format(
            self.first_name,
            self.vk_id,
            self.last_name,
            self.sex,
            self.nickname,
            self.domain,
            self.bdate
        )


# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
# session = Session()
