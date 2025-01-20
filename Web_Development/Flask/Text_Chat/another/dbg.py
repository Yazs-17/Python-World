	from flask import Flask
	from flask_debugtoolbar import DebugToolbarExtension
	
	app = Flask(__name__)
	
	# the toolbar is only enabled in debug mode:
	app.debug = True
	
	# set a 'SECRET_KEY' to enable the Flask session cookies
	app.config['SECRET_KEY'] = '<replace with a secret key>'

	toolbar = DebugToolbarExtension(app)

	@app.route('/')
	def index():
		return '<html><body><h1>这是我的第一个网页程序！</h1></body></html>'
	
	if __name__ == '__main__':
		app.run()
