from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, LargeBinary
from datetime import datetime

engine = create_engine('postgresql://boweldiary:boweldiary@localhost:5432/boweldiary', convert_unicode=True)

session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()


class User(Base):

	__tablename__ = 'users'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	password = Column(String)

	def __repr__(self):
		return "<User(name='%s', id='%s')>" % (self.name, self.id)

	def to_response(self):
		return {'id' : self.id, 'name' : self.name }

class FoodDiaryEntry(Base):

	__tablename__ = 'food_diary'
	id = Column(Integer, primary_key=True)
	created_at = Column(Date, default=datetime.now())
	author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
	content = Column(LargeBinary)

	def to_response(self):
		return { 'id' : self.id, 'author_id' : self.author_id, 'content' : self.content}

#class BowelDiaryEntry(Base):
#
#	__tablename__ = 'bowel_diary'
#	id = Column(Integer, primary_key=True)

Base.metadata.create_all(engine)

#Session = sessionmaker(bind=engine)

#session = Session()
#user = session.query(User).first()#.filter(User.name is 'user1')
#print(user)
#session.add(User(name='user2'))
#session.add(FoodDiaryEntry(author_id=user.id))
#session.commit()