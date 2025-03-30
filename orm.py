from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

"""
作为所有ORM模型的父类，下面所有的ORM模型都是继承自Base，它为所有子类提供了:
1. 表名定义（通过 __tablename__）
2. 列定义能力（通过 Column）
3. 关系定义能力（通过 relationship）
4. 其他SQLAlchemy的ORM特性
所以 Base 主要是为了：
- 简化代码
- 提供统一的接口
- 自动处理很多数据库操作的细节
"""
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    email = Column(String)
    posts = relationship("Post", back_populates="user")
    
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))  # users是users的数据库表名
    user = relationship("User", back_populates="posts")  # 这里提供了user.
