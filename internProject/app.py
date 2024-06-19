from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#test
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


# Define the User model which maps to the 'booking' table in the database
class User(db.Model):
    # Name of the table in the database
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    pitch = db.Column(db.Integer, nullable=False)
    start = db.Column(db.Time, nullable=False)
    end = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)
    amenities = db.Column(db.String(255), nullable=False)

    # Constructor to initialize the User object
    def __init__(self, email, pitch, start, end, date, amenities):
        self.email = email
        self.pitch = pitch
        self.start = start
        self.end = end
        self.date = date
        self.amenities = amenities


@app.route('/')
def index():
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

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/falling')
def falling():
    return render_template('falling.html')

@app.route('/form_r')
def form_r():
    return render_template('form_r.html')


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

# Run the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)