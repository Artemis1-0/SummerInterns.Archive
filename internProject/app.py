from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

# Database configuration
USERNAME = 'root'
PASSWORD = ''
HOST = 'localhost'
DB_NAME = 'vidhur'
# Initialize the Flask application and specify the template and static folders
app = Flask(__name__, template_folder='website/template', static_folder='website/static')
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + USERNAME + ':' + PASSWORD + '@' + HOST + '/' + DB_NAME
# Disable modification tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Set the secret key for session management
app.config['SECRET_KEY'] = 'root'
# Initialize the SQLAlchemy object with the app
db = SQLAlchemy(app)


# Define the Account model for sign-up/sign-in
class Account(db.Model):
    __tablename__ = 'account'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


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


# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/booking')
def booking():
    return render_template('booking.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/nav')
def nav():
    return render_template('nav.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/about_r')
def about_r():
    return render_template('about_r.html')


@app.route('/account')
def account():
    if 'user_id' in session:
        user_id = session['user_id']
        account = Account.query.filter_by(id=user_id).first()
        if account:
            username = account.username
            return render_template('account.html', username=username, logged_in=True)

    # If user is not logged in or account not found, render account.html with default values
    return render_template('account.html', username=None, logged_in=False)


@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signinpage')
def signinpage():
    return render_template('signinpage.html')

# Route for signing up
@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Check if email or username already exists
        existing_user = Account.query.filter((Account.email == email) | (Account.username == username)).first()
        if existing_user:
            flash('Email or username already exists!', 'error')
            return redirect(url_for('signup'))
        new_account = Account(username=username, email=email, password=password)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('signup'))
    return render_template('signup.html')


# Route for signing in
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        account = Account.query.filter_by(email=email, password=password).first()
        if account:
            session['user_id'] = account.id
            username = account.username
            return render_template('account.html', username=username, logged_in=True)
            return redirect(url_for('booking'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('signin.html')


# Route for logging out
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


# Route for the account page



# Route for booking classes
@app.route('/new_booking', methods=['POST'])
def new_booking():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    email = request.form.get('email')
    pitch = request.form.get('pitch')
    start = request.form.get('start')
    end = request.form.get('end')
    date = request.form.get('date')
    amenities = request.form.get('amenities')
    new_booking = Booking(email=email, pitch=pitch, start=start, end=end, date=date, amenities=amenities)
    try:
        db.session.add(new_booking)
        db.session.commit()
        flash('Booking entered successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while booking the class.', 'error')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
