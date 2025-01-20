import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'db\\tlkDB.db')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

manager = Manager(app)
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

#class NameForm(Form):
#    name = StringField('What is your name?', validators=[Required()])
#    submit = SubmitField('Submit')


#@app.errorhandler(404)
#def page_not_found(e):
#    return render_template('404.html'), 404


#@app.errorhandler(500)
#def internal_server_error(e):
#    return render_template('500.html'), 500


#@app.route('/', methods=['GET', 'POST'])
#def index():
#    if form.validate_on_submit():
#        old_name = session.get('name')
#        if old_name is not None and old_name != form.name.data:
#            flash('Looks like you have changed your name!')
#        session['name'] = form.name.data
#        return redirect(url_for('index'))
#    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/')
def index():
    n=CtlkTxt.query.count()
    MtlkTxt = CtlkTxt.query.all()
    i = 0
    tdstr = ""
    while i<n:
        if MtlkTxt[i].own:
            whostr = "我："
            clrstr = "<font color=#ff0000>"
        else:
            whostr = "机器人："
            clrstr =  "<font color=#0000ff>"
        #tdstr = tdstr + clrstr + str(MtlkTxt[i].id) + "," + whostr + "," + MtlkTxt[i].txt + "</font><br />"
        tdstr = tdstr + clrstr + whostr + MtlkTxt[i].txt + "</font><br />"
        i= i + 1
    return render_template('test.html', name=tdstr)

@app.route('/add/')
def add():
    txt_new = CtlkTxt(own = 1, txt = '林强')
    db.session.add(txt_new)
    db.session.commit()
    return 'Add Ok!'

if __name__ == '__main__':
    manager.run()
