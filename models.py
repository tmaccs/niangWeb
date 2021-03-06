#encoding:utf-8
#存放各种模型
from exts import db
from datetime import datetime
#用db定义各种模型
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import text

class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    telephone = db.Column(db.String(11),nullable=False)
    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.Text,nullable=False)

    # 拦截用户输入的三个信息
    def __init__(self,*args,**kwargs):
        telephone=kwargs.get('telephone')
        username =kwargs.get('username')
        password=kwargs.get('password')

        self.telephone=telephone
        self.username=username
        self.password= generate_password_hash(password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result


class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(50),nullable=False)
    content = db.Column(db.Text,nullable=False)
    # 被阅读次数
    viewsnum = db.Column(db.Integer,server_default=text('0'))

    #注意datetime.now后面不加(),加了括号就是服务器第一次运行的时间，不加则是每次创建一个模型的时候获取的当前的时间
    create_time = db.Column(db.DateTime,default=datetime.now)
    #绑定一个外键
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('Users',backref=db.backref('questions'))

    def increace_viewsnum(self):
        # 这样添加是错误的，只能是add一个完整的数据，add可以修改已有的数据
        # self.viewsnum += 1
        # db.session.add(self.viewsnum)
        # db.session.commit()
        question = Question.query.get(self.id)
        question.viewsnum += 1
        db.session.add(question)
        db.session.commit()


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    #answer_num = db.Column(db.Integer, nullable=False)
    #答案需要和对应的问题，和此时登录的人绑定在一起
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('Users',backref=db.backref('answers'))
    question = db.relationship('Question',backref=db.backref('answers'))