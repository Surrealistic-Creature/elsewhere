from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from config import pstgr



engine = create_engine('postgresql://{}:{}@localhost/elsewhere'.format(pstgr['login'], pstgr['pass']), echo=True)
Base = declarative_base()

# class City(Base):


class VKFriend(Base):
    __tablename__ = 'friends'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    vk_id = Column(Integer)
    last_name = Column(String)
    sex = Column(Integer)
    nickname = Column(String)
    domain = Column(String)
    def __repr__(self):
        return ("Person("
            "first_name='{}',"
            "vk_id={},"
            "last_name='{}',"
            "sex={},"
            "nickname='{}',"
            "domain='{}')").format(
            self.first_name,
            self.vk_id,
            self.last_name,
            self.sex,
            self.nickname,
            self.domain,
            )


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
# session = Session()
