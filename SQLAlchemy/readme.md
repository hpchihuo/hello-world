操作环境：实验楼已经搭建好的Linux下的环境，并安装好了MySQL客户端与服务端

代码主要运用了三个个库
SQLAlchemy：操作sql
faker：创建模拟数据
random：随机选择

SQLAlchemy：创建引擎
疑问：1.为什么要加mysqldb？mysql+python来连接
2.hostname可以写成ip+port的格式？

engine = create_engine('mysql+mysqldb'://username:passwd@hostname/database)

Base = declarative_base() #建立表模型时需要用到，具体是什么原理？

创建表模型：
class Host(Base):
	pass

列名创建：id = Column(Integer, primary_key=True, autoincrement=True) #创建主键
Column:参数
数据类型：Integer， String， Text， Boolean，SmallInteger，Datetime
nullable：数据可否为空
index：创建索引

Base.metadata.create_all(engine) #将创建的表的模型提交到Mysql，一旦提交后，SQLAlchemy不支持修改表的结构

建立一对多关系：
__tablename__ = "users"     #表users
__tablename__ = "articles"  #表articles

articles = relationship('Article') #在User中建立与Article关系

#user_id = Column(Integer, ForeinKey('users.id'))
#author = relationship('User') #在Article中建立与User关系

使用backref，只需在User中建立关系
articles = relationship('Article', backref='author')


建立一对一关系
userinfo = relationship('UserInfo', backref='user',uselist=False) #uselist默认为True，即一对多


多对多关系:通过建立辅助表来建立关系，
article_tag = Table(
	#表名，与metadata参数，固定且必须
	'article_tag', Base.metadata,
	#存储两个表的id，设置外键
	Colume('article_id', Integer, ForeighKey('articles.id')),
	Column('tag_id', Integer, ForeignKey('tags.id'))
	)

通过Session来插入数据

Session = sessionmaker(bing=engine)
session = Session()

插入一条数据
uerdata = [User(username,passwd,email)]
session.add_all(usedata)
session.commit()



faker库
faker = Factory.create() #创建一个工厂对象
faker.word()
faker.name()
faker.email()
faker.sentence()
faker.sentences(n)#生成n句话组成的列表


random库
random.choice(list)
random.randint(n1, n2)#生成n1到n2的随机数，闭区间
