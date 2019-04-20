import flask
import flask_wtf
import wtforms


class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired(),
                                                           wtforms.validators.Length(min=2, max=20)])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])

    submit = wtforms.SubmitField('Login')


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'sonobello'


@app.route('/')
def index():
    return 'Hello, World! Index page.'

@app.route('/slideshow/<int:index>')
def slideshow(index):
    return flask.render_template('slideshow.html', title='aaa', time='00:00', image_path='', index=index)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flask.flash('Logged in. Not really just a test.', 'success')
    return flask.render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=80)
