import flask
import flask_wtf
import wtforms
import os

import json_file


class LoginForm(flask_wtf.FlaskForm):
    username = wtforms.StringField('Username', validators=[wtforms.validators.DataRequired(),
                                                           wtforms.validators.Length(min=2, max=20)])
    password = wtforms.PasswordField('Password', validators=[wtforms.validators.DataRequired()])

    submit = wtforms.SubmitField('Login')


app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'sonobello'

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
        return flask.redirect('/slideshow/' + form.username.data + '/1')
    return flask.render_template('login.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=80)
