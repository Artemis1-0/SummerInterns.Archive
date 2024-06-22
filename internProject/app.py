from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm)
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember')


app = Flask(__name__, template_folder='website/template', static_folder='website/static')
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    form = LoginForm()

    return render_template('login.html', form=form)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)