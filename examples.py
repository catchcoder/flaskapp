from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

@app.route('/')
def index():
    return 'Hello world'


@app.route('/profile/<username>')
def profile(username):
    return 'This is the user profile for {}'.format(username)


@app.route('/id/<int:post_id>')
def id(post_id):
    return ('The post id is={}'.format(post_id))

@app.errorhandler(404)
def error():
    return ('error')


if __name__ == '__main__':
    app.run(debug=True)
