import os

from flask import abort, flash, Flask, jsonify, render_template, redirect, request
from flask_login import current_user, LoginManager, login_required, login_user, logout_user
from wtforms import PasswordField, StringField, SubmitField, BooleanField
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

from models import ADMIN_USER, AnonymousUser, CREATOR_USER, Course, GUEST_USER, NORMAL_USER, Progress, User, Slide


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    creator = BooleanField('Creator')
    submit = SubmitField('Login')


@app.route('/')
def index():
    return render_template('index.html', next='/')


@login_required
@app.route('/<string:username>/<string:course_name>', methods=['GET', 'POST'])
def slideshow(username, course_name):
    user = User.query.filter_by(username=username).first_or_404()
    course = Course.query.filter_by(name=course_name, owner=user.id).first_or_404()
    if request.method == 'POST':
        data = request.json
        slide_index = data.get('index')
        if slide_index:
            progress = Progress(user_id=user.id, course_id=course.id, index=slide_index)
            db.session.add(progress)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return abort(400)
    else:
        slide_index = Progress.query.filter_by(user_id=user.id, course_id=course.id).first()
        slide_index = slide_index.index if slide_index else 0 
        return render_template('slideshow.html', index=slide_index, user=current_user, slides=course.slides, next=request.path)


@login_required
@app.route('/manager')
def manager():
    return render_template('manager.html')


@login_required
@app.route('/<string:username>/<string:course_name>/edit', methods=['GET', 'POST'])
def edit_slideshow(username, course_name):
    user = User.query.filter_by(username=username).first_or_404()
    course = Course.query.filter_by(name=course_name, owner=user.id).first_or_404()
    if hasattr(current_user, 'role') and getattr(current_user, 'role') >= CREATOR_USER:
        slides = Slide.query.all()
        safe_username = secure_filename(user.username)
        safe_coursename = secure_filename(course.name)
        course_folder = '/' + '/'.join(['static', 'users', safe_username, safe_coursename])
        images = os.listdir(os.path.join('static', 'users', safe_username, safe_coursename))
        for index, image in enumerate(images):
            images[index] = course_folder + '/' + image
        if request.method == 'POST':
            data = request.json
            for slide in slides:
                db.session.delete(slide)
            for slide_dict in data:
                slide = Slide(title=slide_dict.get('title'), image=slide_dict.get('image'), time=slide_dict.get('time'), course_id=course.id)
                db.session.add(slide)
            db.session.commit()
            return jsonify({'success': True}), 200
        else:
            return render_template('admin.html', slides=slides, images=images, next='/', enumerate=enumerate)
    else:
        return abort(404)


@login_required
@app.route('/<string:username>/<string:course_name>/upload', methods=['POST'])
def upload_image(username, course_name):
    user = User.query.filter_by(username=username).first_or_404()
    course = Course.query.filter_by(name=course_name, owner=user.id).first_or_404()
    try:
        image = request.files['image']
        folder = os.path.join('static', 'users', secure_filename(user.username), secure_filename(course.name))
        if not os.path.isdir(folder):
            os.makedirs(folder)
        image.save(os.path.join(folder, secure_filename(image.filename)))
        return jsonify({'success': True}), 200
    except OSError as e:
        return jsonify({'error': str(e), 'status': 500, 'success': False}), 500


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
            user = User(username=form.username.data, password=form.password.data, role=CREATOR_USER if form.creator.data else NORMAL_USER)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            user_folder = os.path.join('static', 'users', secure_filename(form.username.data))
            if not os.path.isdir(user_folder):
                os.mkdir(user_folder)
            flash('Registration successful!', 'success')
        path = request.args.get('redirect')
        path = path if path else '/'
        return redirect(path)
    return render_template('login.html', form=form, next=request.path)


@login_required
@app.route('/logout')
def logout():
    path = request.args.get('redirect')
    path = path if path else '/'
    logout_user()
    return redirect(path)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()
