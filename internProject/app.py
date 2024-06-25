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


class Account(db.Model):
    __tablename__ = 'account'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)



class Booking(db.Model):
    __tablename__ = 'booking'  # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    pitch = db.Column(db.Integer, nullable=False)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    amenities = db.Column(db.String(255), nullable=False)

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

@app.route('/vdnav')
def vdnav():
    return render_template('vdnav.html')



@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/about_r')
def about_r():
    return render_template('about_r.html')

@app.route('/form_r')
def form_r():
    return render_template('form_r.html')

@app.route('/account_r')
def account_r():
    return render_template('account_r.html', username=None, logged_in=False, bookings=[])


# Check for overlapping bookings
def is_booking_conflict(pitch, start, end, date, exclude_booking_id=None):
    query = Booking.query.filter_by(pitch=pitch, date=date)
    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)

    existing_bookings = query.all()
    for booking in existing_bookings:
        booking_start = booking.start.strftime('%H:%M')
        booking_end = booking.end.strftime('%H:%M')
        if (start < booking_end and end > booking_start):
            return True
    return False


@app.route('/new_booking', methods=['POST'])
def new_booking():
    if 'user_id' not in session:
        return redirect(url_for('signinpage'))

    user_id = session['user_id']
    user_account = Account.query.filter_by(id=user_id).first()

    if not user_account:
        return redirect(url_for('signinpage'))

    email = user_account.email  # Retrieve the email from the user's account
    pitch = request.form.get('pitch')
    start = request.form.get('start')
    end = request.form.get('end')
    date = request.form.get('date')
    amenities = request.form.get('amenities')

    # Check for booking conflicts
    if is_booking_conflict(pitch, start, end, date):
        flash('The pitch is already booked for the selected time.', 'error')
        return redirect(url_for('booking'))

    new_booking = Booking(email=email, pitch=pitch, start=start, end=end, date=date, amenities=amenities)

    try:
        db.session.add(new_booking)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while booking the pitch.', 'error')

    return redirect(url_for('home'))
@app.route('/edit_booking/<int:booking_id>', methods=['POST'])
def edit_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    pitch = request.form['pitch']
    start = request.form['start']
    end = request.form['end']
    date = request.form['date']
    amenities = request.form['amenities']

    # Check for booking conflicts
    if is_booking_conflict(pitch, start, end, date, exclude_booking_id=booking_id):
        flash('The pitch is already booked for the selected time.', 'error')
        return redirect(url_for('account'))

    booking.pitch = pitch
    booking.start = start
    booking.end = end
    booking.date = date
    booking.amenities = amenities

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating the booking.', 'error')

    return redirect(url_for('account'))


@app.route('/account')
def account():
    if 'user_id' in session:
        user_id = session['user_id']
        account = Account.query.filter_by(id=user_id).first()
        if account:
            username = account.username
            bookings = Booking.query.filter_by(email=account.email).all()
            return render_template('account.html', username=username, logged_in=True, bookings=bookings)

    return render_template('account.html', username=None, logged_in=False, bookings=[])


@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/ts')
def ts():
    return render_template('ts.html')

@app.route('/signinpage')
def signinpage():
    return render_template('signinpage.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Check if email or username already exists
        existing_user = Account.query.filter((Account.email == email) | (Account.username == username)).first()
        if existing_user:
            return redirect(url_for('signinpage'))
        new_account = Account(username=username, email=email, password=password)
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('signinpage'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        account = Account.query.filter_by(email=email, password=password).first()
        if account:
            session['user_id'] = account.id
            return redirect(url_for('account'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('signin.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('account'))





@app.route('/delete_booking/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    try:
        db.session.delete(booking)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while deleting the booking.', 'error')

    return redirect(url_for('account'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404  

if __name__ == '__main__':
    app.run(debug=True)
