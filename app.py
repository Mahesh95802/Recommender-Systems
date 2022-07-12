from pickle import FALSE, TRUE
from flask import Flask, render_template, redirect, url_for, request, json, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from matplotlib.pyplot import title 
from wtforms import StringField, PasswordField, BooleanField, SelectField, validators
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd

from python.FilteringSuggestions import filteringSuggestions

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = FALSE
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class ViewershipHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15))
    moviename = db.Column(db.String(200))

possible_names = {'0': 'hans', '1': 'sepp', '3': 'max'}

class movies(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    movieId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    genres = db.Column(db.String(200))
    rating = db.Column(db.Float)

    def as_dict(self):
        return {'name': self.title}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class MovieSearchForm(FlaskForm):
    moviename = StringField("Movie", validators=[InputRequired()])

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
        return redirect(url_for('message', message="Incorrect Credentials!!"))
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        try:
            new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('message', message="New User has been Created!!"))
        except:
            return redirect(url_for('message', message="User already exists!!"))
    return render_template('signup.html', form=form)

@app.route('/message')
def message():
    msg = request.args.get('message', None) 
    return render_template('message.html', message=msg)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = MovieSearchForm()
    if form.validate_on_submit():
        movienames = movies.query.add_columns(movies.title).all()
        movienames = [ j for i,j in movienames]
        if form.moviename.data in movienames:
            usermovielist = ViewershipHistory.query.join(movies, movies.title==ViewershipHistory.moviename).add_columns(movies.title).filter(ViewershipHistory.username==current_user.username).all()
            usermovielist = [ j for i,j in usermovielist]
            if form.moviename.data not in usermovielist:
                try:
                    new_movie = ViewershipHistory(username=current_user.username, moviename=form.moviename.data)
                    db.session.add(new_movie)
                    db.session.commit()
                except:
                    return redirect(url_for('dashboard'))
        return redirect(url_for('dashboard'))
    else:
        movielist = ViewershipHistory.query.join(movies, movies.title==ViewershipHistory.moviename).add_columns(ViewershipHistory.id, ViewershipHistory.username, movies.movieId, movies.title, movies.genres, movies.rating).filter(ViewershipHistory.username==current_user.username).all()
        return render_template('dashboard.html', name=current_user.username, form=form, movielist=movielist)

@app.route('/movies')
@login_required
def moviedic():
    movienames = movies.query.add_columns(movies.title).all()
    movienames = [ j for i,j in movienames]
    return jsonify(movienames)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    history_to_delete = ViewershipHistory.query.get_or_404(id)
    try:
        db.session.delete(history_to_delete)
        db.session.commit()
        return redirect(url_for('dashboard'))
    except:
        return redirect(url_for('message', message="There was a problem deleting that Record!!"))

@app.route('/recommendations')
@login_required
def recommendations():
    movieList = ViewershipHistory.query.join(movies, movies.title==ViewershipHistory.moviename).add_columns(ViewershipHistory.id, ViewershipHistory.username, movies.movieId, movies.title, movies.genres, movies.rating).filter(ViewershipHistory.username==current_user.username).all()
    movieNames = [ movie.title for movie in movieList]
    movieRecommendations = filteringSuggestions(movieNames)
    movieDf = pd.DataFrame(movies.query.add_columns(movies.movieId, movies.title, movies.genres, movies.rating).all())
    movieDf.drop(["movies"], axis=1)
    recommendationList = pd.merge(left = movieRecommendations, right = movieDf, how = 'inner', on = 'title' )
    #print(recommendationList.head())
    return render_template('recommendations.html', name=current_user.username, movielist=recommendationList)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
