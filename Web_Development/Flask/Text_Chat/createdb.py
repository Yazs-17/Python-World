import os
from flask import Flask
from flask_script import Server, Manager
from flask_sqlalchemy import SQLAlchemy
#导入数据库支持模块SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))   #获取应用程序路径

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'db\\tlkDB.db')
#设置数据库为运行文件目录下的db\tlkDB.db
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
server = Server(host="0.0.0.0", port=80, threaded=True)
manager.add_command("runserver", server)
db = SQLAlchemy(app) #建立应用app的数据库对象db

#定义表tlkTxt的模型CltkTxt，在Python代码中CltkTxt就代表tlkTxt表。
class CtlkTxt(db.Model):
    __tablename__ = 'tlkTxt'
    id = db.Column(db.Integer, primary_key=True, index=True)
    own = db.Column(db.Integer)
    txt = db.Column(db.String(256))

    def __repr__(self):
        return '<CtlkTxt %r>' % self.txt

if __name__ == '__main__':
    db.create_all()      #创建数据库db\tlkDB.db
    manager.run()
