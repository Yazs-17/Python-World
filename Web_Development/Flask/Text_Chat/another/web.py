from flask import Flask
from flask_script import Server, Manager
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
print(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<replace with a secret key>'
toolbar = DebugToolbarExtension(app)
manager = Manager(app)
server = Server(host="0.0.0.0", port=80)
manager.add_command("runserver", server)



@app.route('/')
def index():
    return '<body><h1>这是我的第一个网页程序！</h1></body>'


if __name__ == '__main__':
    manager.run()
