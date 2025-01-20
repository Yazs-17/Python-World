#SSH，再次测试SSH
import os
from flask import Flask, render_template, session, redirect, url_for, flash
#from flask_debugtoolbar import DebugToolbarExtension
from flask_script import Server, Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

import sys
sys.path.insert(0, "../")

import aiml

k = aiml.Kernel()
k.learn("cn-startup.xml")
k.respond("load aiml cn")
k.respond("start")

basedir = os.path.abspath(os.path.dirname(__file__))
                          
app = Flask(__name__)
app.config['SECRET_KEY'] = '<replace with a secret key>'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'db\\tlkDB.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.debug = True
#toolbar = DebugToolbarExtension(app)

manager = Manager(app)
#server = Server(host="0.0.0.0", port=80, use_debugger=True)
server = Server(host="0.0.0.0", port=80)
manager.add_command("runserver", server)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class CtlkTxt(db.Model):
    __tablename__ = 'tlkTxt'
    id = db.Column(db.Integer, primary_key=True, index=True)
    own = db.Column(db.Integer)
    txt = db.Column(db.String(256))

    def __repr__(self):
        return '<CtlkTxt %r>' % self.txt


class NameForm(FlaskForm):                 
    name = StringField('请开始交谈：', validators=[DataRequired()])
    submit = SubmitField('提交')
#    submit1 = SubmitField('清除')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    name = ''
    rp_name = ''
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        rp_name = k.respond(name)
        if rp_name == "":
            rp_name = "......(沉默）"
        my_txt = CtlkTxt(own = 1, txt = name)
        robot_txt = CtlkTxt(own = 0, txt = rp_name)
        db.session.add(my_txt)
        db.session.add(robot_txt)
        db.session.commit()
        
    n = CtlkTxt.query.count()
    MtlkTxt = CtlkTxt.query.all()
    i = 0
    tdstr = ''
    while i<n:
        if MtlkTxt[i].own:
            whostr = "我："
            clrstr = "<font color=#ff0000>"
        else:
            whostr = "机器人："
            clrstr = "<font color=#0000ff>"
        tdstr = tdstr + clrstr + whostr + MtlkTxt[i].txt + "</font><br />"
        i = i+1
        
    return render_template('index.html', tdstr=tdstr, form=form, name=rp_name)

#@app.route('/')
#def index():
#    return render_template('index.html')


#@app.route('/talk/<word>')
#def talk(word):
#    return render_template('user.html', webword=k.respond(word))


if __name__ == '__main__':
    manager.run()
#    app.run()
#    app.run(debug=True)
