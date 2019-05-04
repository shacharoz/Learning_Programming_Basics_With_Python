import secrets
import os

import flask
import flask_wtf
import wtforms
import flask_login
import flask_sqlalchemy

import json_file

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'sonobello'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

db = flask_sqlalchemy.SQLAlchemy(app)

users_json = json_file.JsonFile('users.json')
users_json.load()

slides_json = json_file.JsonFile(os.path.join('static', 'dat/slides.json'))
slides_json.load()
slides = slides_json.data


class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired(),
                                                           wtforms.validators.Length(min=2, max=20)])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])

    submit = wtforms.SubmitField('Login')


class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def get_id(self):
        return self.id


@app.route('/')
def index():
    return 'Hello, World! Index page.'


@app.route('/slideshow/<int:_index>')
@flask_login.login_required
def slideshow(_index):
    slide = slides[_index - 1]
    user = flask_login.current_user
    return flask.render_template('slideshow.html', title=slide['title'], time=slide['time'], image_path=slide['image'],
                                 index=_index - 1, back=_index != 1, next=_index < len(slides), user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # flask.flash('Logged in. Not really just a test.', 'success')
        if db.session.query(
                db.session.query(User).filter_by(username=form.username.data).exists()
        ).scalar():
            flask_login.login_user(User.query.filter_by(username=form.username.data).first())
        else:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flask_login.login_user(user)
        return flask.redirect('/slideshow/1')
    return flask.render_template('login.html', form=form)


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


if __name__ == '__main__':
    app.run(debug=True, port=80)
