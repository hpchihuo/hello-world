# coding: utf-8

from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker
from faker import Factory
import random

#建立与mysql的连接，通过python
engine = create_engine('mysql+mysqldb://root@localhost:3306/blog')

#建立名为Base的类，建立表模型时继承该类
Base = declarative_base()

#创建一个表
class User(Base):
	#表名为users
	__tablename__ = 'users'
	#表的属性，主键id，其他列属性username,password,email
	id = Column(Integer, primary_key=True)
	username = Column(String(64), nullable=False, index=True)
	password = Column(String(64), nullable=False)
	email = Column(String(64), nullable=False, index=True)
	#建立与Article的关系，一对多
	articles = relationship('Article', backref = 'author')
	#建立与UserInfo的关系，多对多
	userinfo = relationship('UserInfo',backref = 'user', uselist=False)
	#测试用？
	def __repr__(self):
		return '%s(%r)'%(self.__class__.__name__, self.username)
#创建名为articles的表，列属性包括id,title,content,user_id,cate_id
class Article(Base):
	__tablename__ = 'articles'

	id = Column(Integer, primary_key=True)
	title = Column(String(255), nullable=False, index=True)
	content = Column(Text)
	#建立外键，外键为users.id
	user_id = Column(Integer, ForeignKey('users.id'))
	cate_id = Column(Integer, ForeignKey('categories.id'))
	tags = relationship('Tag', secondary='article_tag', backref='articles')
#创建名为categories的表
class Category(Base):

	__tablename__ = "categories"

	id = Column(Integer, primary_key=True)
	name = Column(String(64), nullable=False, index=True)
	articles = relationship('Article', backref='category')
#创建名为userinfos的表，用户详细信息
class UserInfo(Base):

	__tablename__ = 'userinfos'

	id = Column(Integer, primary_key=True)
	name = Column(String(64))
	qq = Column(String(11))
	phone = Column(String(11))
	link = Column(String(64))
	user_id = Column(Integer, ForeignKey('users.id'))

#建立多对多辅助表，文章与文章标签的对应关系
article_tag = Table(
	'article_tag', Base.metadata,
	Column('article_id', Integer, ForeignKey('articles.id')),
	Column('tag_id', Integer, ForeignKey('tags.id'))
	)
#创建tags表
class Tag(Base):

	__tablename__ = 'tags'

	id = Column(Integer, primary_key=True)
	name = Column(String(64), nullable=False, index=True)

if __name__=='__main__':
	#提交表模型到mysql，mysql生成表
	Base.metadata.create_all(engine)
	#创建模拟数据工厂
	faker = Factory.create()
	#创建Session，通过session提交数据
	Session = sessionmaker(bind=engine)
	session = Session()
	#创建由10个User类组成的列表，每个类里面已传入users表的列属性数据
	faker_users = [User(
		username = faker.name(),
		password = faker.word(),
		email = faker.email(),
		) for i in range(10)]
	#提交数据到session保存
	session.add_all(faker_users)
	#创建5个Category组成的列表
	faker_categories = [Category(name=faker.word()) for i in range(5)]
	#提交数据到session保存
	session.add_all(faker_categories)
	#创建20个Tag组成的列表
	faker_tags = [Tag(name=faker.word()) for i in range(20)]
	#提交数据到session保存
	session.add_all(faker_tags)
	#创建100个Article类数据
	for i in range(100):
		article = Article(
			title=faker.sentence(),
			content=' '.join(faker.sentences(nb=random.randint(10, 20))),
			author=random.choice(faker_users),
			category=random.choice(faker_categories)
			)
		#在生成的标签fakers_tag中，随机选取2-5个
		for tag in random.sample(faker_tags, random.randint(2, 5)):
			#将标签连接到articles的外键属性上
			article.tags.append(tag)
		#提交一个数据到session保存
		session.add(article)

	session.commit()