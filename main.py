from flask import Flask, session, url_for, redirect, request
from flask_session import Session
import requests
import json
from time import sleep

serverUrl = 'http://localhost'
serverPort = '89'
clientID = 'put your clientID here'
clientSecret = 'put your clientSecret here'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'demoSecretKey'  # remember change this
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


@app.route('/')
def index():
    if session.get('access_token') is None:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET'])
def login():
    if request.args.get('code') is not None:
        params = {
            'grant_type': 'authorization_code',
            'client_id': clientID,
            'client_secret': clientSecret,
            'code': request.args.get('code')
        }
        while 1:
            try:
                r = json.loads(requests.get('https://api.hduhelp.com/oauth/token', params=params).text)
                if r['error'] == 0:
                    session['access_token'] = r['data']['access_token']
                    return session['access_token']
            except:
                print('get data failed')
                sleep(0.5)
    if session.get('access_token') is None:
        return redirect('https://api.hduhelp.com/oauth/authorize?response_type=code&client_id={}&redirect_uri={}&state={}'.format(clientID, str((serverUrl + ':' + serverPort + '/login').encode())[2:-1], '666'))


@app.route('/token')
def token():
    return str(session.get('access_token'))


@app.route('/logout')
def logout():
    if session.get('access_token') is not None:
        session.pop('access_token')
        return 'logout successfully'
    return "haven\'t login"


@app.route('/info/basic')
def infoBasic():
    if session.get('access_token') is None:
        return redirect(url_for('login'))
    header = {
        'Authorization': 'token '+session['access_token']
    }
    while 1:
        try:
            return requests.get('https://api.hduhelp.com/base/person/info', headers=header).text
        except:
            print('get data failed')
            sleep(0.5)


@app.route('/info/detail')
def infoDetail():
    if session.get('access_token') is None:
        return redirect(url_for('login'))
    header = {
        'Authorization': 'token '+session['access_token']
    }
    while 1:
        try:
            return requests.get('https://api.hduhelp.com/base/student/info', headers=header).text
        except:
            print('get data failed')
            sleep(0.5)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=serverPort)  # remember to change debug to False
