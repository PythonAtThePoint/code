from flask import Flask
from flask import request
from flask import send_file
from B002_Magical_Web_Servers import lastcol
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World"


@app.route('/meow')
def something():
    print(request)
    return 'got it!'


@app.route('/lastfm/<username>')
def last_fm(username):
    try:
        collage = lastcol.LastFMImage(username)
        return send_file(collage.path, mimetype='image/gif')
    except lastcol.LastFMError as e:
        return str(e)  # 'Error with lastfm'


app.run(debug=True)
