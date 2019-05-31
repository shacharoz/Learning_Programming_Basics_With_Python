import os

from flask import abort, flash, Flask, jsonify, render_template, redirect, request
from flask_login import current_user, LoginManager, login_required, login_user
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

from filters import do_tojson


app = Flask(__name__)
app.config['SECRET_KEY'] = 'This is a secret! ;) Sshh...'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

app.jinja_env.filters['tojson'] = do_tojson

login_manager = LoginManager()
login_manager.init_app(app)

db = SQLAlchemy(app)

from models import ADMIN_USER, AnonymousUser, GUEST_USER, NORMAL_USER, User, Slide 


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


@app.route('/')
def index():
    return redirect('login')


@login_required
@app.route('/slideshow', methods=['GET', 'POST'])
def slideshow():
    if request.method == 'POST':
        data = request.json
        index = data.get('index')
        if index:
            current_user.progress = index
            db.session.commit()
            return jsonify({ 'success': True })
        else:
            return abort(400)
    else:
        slides = Slide.query.all()
        slide_index = current_user.progress if current_user.progress else 0
        return render_template('slideshow.html', index=slide_index, user=current_user, slides=slides)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if db.session.query(db.session.query(User).filter_by(username=form.username.data).exists()).scalar():
            user = User.query.filter_by(username=form.username.data).first()
            if form.password.data == user.password:
                login_user(user)
                flash('Login successful!', 'success')
            else:
                flash('Login failed!', 'danger')
                return redirect('login')
        else:
            user = User(username=form.username.data, password=form.password.data, role=ADMIN_USER)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Registration successful!', 'success')
        if user.role == ADMIN_USER:
            return redirect('slideshow/edit')
        else:
            return redirect('/slideshow/' + str(user.progress if user.progress is not None else 1))
    return render_template('login.html', form=form)


@login_required
@app.route('/slideshow/edit', methods=['GET', 'POST'])
def edit_slideshow():
    if hasattr(current_user, 'role') and getattr(current_user, 'role') == ADMIN_USER:
        slides = Slide.query.all()
        images = os.listdir(os.path.join('static', 'img'))
        if request.method == 'POST':
            data = request.json
            for slide in slides:
                db.session.delete(slide)
            for slide_dict in data:
                slide = Slide(title=slide_dict.get('title'), image=slide_dict.get('image'), time=slide_dict.get('time'))
                db.session.add(slide)
            db.session.commit()
            return jsonify({'success': True}), 200
        else:
            return render_template('admin.html', slides=slides, images=images, enumerate=enumerate)
    else:
        return abort(404)


@login_required
@app.route('/slideshow/upload', methods=['POST'])
def upload_image():
    try:
        image = request.files['image']
        image.save(os.path.join('static', 'img', secure_filename(image.filename)))
        return jsonify({ 'success': True }), 200
    except OSError as e:
        return jsonify({ 'error': str(e), 'status': 500, 'success': False }), 500


@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()


if __name__ == '__main__':
    app.run(debug=True, port=80)
