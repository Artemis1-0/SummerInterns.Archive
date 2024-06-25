from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

USERNAME = 'root'
PASSWORD = ''
HOST = 'localhost'
DB_NAME = 'vidhur'

app = Flask(__name__, template_folder='website/template', static_folder='website/static')
app.config['SECRET_KEY'] = 'topsecret!'
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    __tablename__ = 'account'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Define the Booking model
class Booking(db.Model):
    __tablename__ = 'booking'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    pitch = db.Column(db.Integer, nullable=False)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    amenities = db.Column(db.String(255), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message = 'Invalid Email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

@app.route('/')
def home():
    register_form = RegisterForm()
    login_form = LoginForm()
    return render_template('home.html', register_form=register_form, login_form=login_form)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/admin')
def admin():
    return render_template('admin.html', username=None, logged_in=False, bookings=[])

@app.route('/login', methods=['GET', 'POST'])
def login():
    register_form = RegisterForm()
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.password == form.password.data:
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))
            
        return '<h1> Invalid Username or Password </h1>'

    return render_template('dashboard.html', register_form=register_form, login_form=login_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    login_form = LoginForm()

    if register_form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
       
    return render_template('login.html', register_form=register_form, login_form=login_form)

@app.route('/form_r')
def form_r():
    register_form = RegisterForm()
    login_form = LoginForm()
    return render_template('form_r.html', register_form=register_form, login_form=login_form)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/booking')
@login_required
def booking():
    return render_template('booking.html')

# Define the route to handle form submission for entering a submission
@app.route('/booking', methods=['POST'])
def enter_name():
    # Retrieve everything from the form data
    email = request.form.get('email')
    pitch = request.form.get('pitch')
    start = request.form.get('start')
    end = request.form.get('end')
    date = request.form.get('date')
    amenities = request.form.get('amenities')
    # Create a new User object with the form data
    new_name = User(email=email, pitch=pitch, start=start, end=end, date=date,amenities=amenities)

    try:
        # Attempt to add the new User object to the database
        db.session.add(new_name)
        # Commit the transaction
        db.session.commit()
        print('Name entered successfully!')
    except Exception as e:
        # If an error occurs, roll back the transaction
        db.session.rollback()
        print('An error occurred while booking the class.')


    # Redirect to the booking page after form submission
    return redirect(url_for('booking'))
#test

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404  

if __name__ == '__main__':
    app.run(debug=True)