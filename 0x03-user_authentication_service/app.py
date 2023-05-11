#!/usr/bin/env python3
'''api for basic user operation with authentication'''
from auth import Auth
from flask import (Flask,
                   jsonify,
                   request,
                   abort,
                   redirect)

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index() -> str:
    '''inded route handler'''
    res = {"message": "Bienvenue"}
    return jsonify(res)


@app.route('/users', methods=['POST'])
def register_user() -> str:
    '''Registers new user if it does not exist'''
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    res = {"email": email, "message": "user created"}
    return jsonify(res)


@app.route('/sessions', methods=['POST'])
def log_in() -> str:
    '''Logs in user and returns session ID'''
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)
    if not AUTH.valid_login(email, password):
        abort(401)
    session_id = AUTH.create_session(email)
    res_msg = {"email": email, "message": "logged in"}
    res = jsonify(res_msg)
    res.set_cookie("session_id", session_id)
    return res


@app.route('/sessions', methods=['DELETE'])
def log_out() -> str:
    '''locates user with session id, destroys session and redirects user
    to index route'''
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    '''checks if user exists and returns user's email with 200
    status code'''
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    res = {"email": user.email}
    return jsonify(res), 200


@app.route('/reset_password', methods=['POST'])
def reset_password() -> str:
    '''generates and returns a reset token for registered user'''
    try:
        email = request.form['email']
    except KeyError:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    res = {"email": email, "reset_token": reset_token}
    return jsonify(res), 200


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    '''updates user's password using reset token'''
    try:
        email = request.form['email']
        reset_token = request.form['reset_token']
        new_password = request.form['new_password']
    except KeyError:
        abort(400)
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)
    res = {"email": email, "message": "Password updated"}
    return jsonify(res), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
