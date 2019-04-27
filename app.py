import flask
import flask_wtf
import wtforms
import flask_login
import secrets

import os

import json_file


class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired(),
                                                           wtforms.validators.Length(min=2, max=20)])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])

    submit = wtforms.SubmitField('Login')


class User(flask_login.UserMixin):

    @classmethod
    def gen_id(cls):
        value = secrets.token_hex(32)
        print(value)
        valid = True
        for name, data in users_json.data.items():
            print(name, data)
            if data['id'] == value:
                valid = False
                break
        print(valid)
        if valid:
            return value
        else:
            return cls.gen_id()

    def register(self, username, password):
        self.username = username
        self.password = password
        users_json.data[self.username] = {'password': password, 'id': self.id}
        users_json.save()

    def load(self, user_data):
        self.password = user_data['password']
        self.id = user_data['id']

    def __init__(self, username, password=None):
        user_data = users_json.data.get(username)
        if username in users_json.data:
            self.load(user_data)
        else:
            self.id = self.gen_id()
            self.register(username, password)


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'sonobello'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users_json = json_file.JsonFile('users.json')
users_json.load()

slides_json = json_file.JsonFile(os.path.join('static', 'dat/slides.json'))
slides_json.load()
slides = slides_json.data


@app.route('/')
def index():
    return 'Hello, World! Index page.'


@app.route('/slideshow/<string:username>/<int:_index>')
def slideshow(username, _index):
    slide = slides[_index - 1]
    return flask.render_template('slideshow.html', title=slide['title'], time=slide['time'], image_path=slide['image'],
                                 index=_index - 1, back=_index != 1, next=_index < len(slides), username=username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        #flask.flash('Logged in. Not really just a test.', 'success')
        flask_login.login_user(User(form.username.data, form.password.data))
        return flask.redirect('/slideshow/' + form.username.data + '/1')
    return flask.render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return None


if __name__ == '__main__':
    app.run(debug=True, port=80)
