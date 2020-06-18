from flask import Flask, url_for, redirect, session, render_template
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = 'random secret'

#https://docs.authlib.org/en/latest/basic/index.html
#oauth config
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='495451370244-vmk79jh8653v4t8719cb26m4eil8j4le.apps.googleusercontent.com',
    client_secret='OlOWxgzZM2M2_iVoUQjAevgx',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/home')
def home():
    email = dict(session).get('email',None)
    #return f'Hello, {email}!'
    return render_template('home.html', email=email)


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']
    return redirect('/home')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

