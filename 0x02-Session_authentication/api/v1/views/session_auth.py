#!/usr/bin/env python3
'''session authentication routes'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    '''fetches and returns user detail'''
    email = request.form.get('email')

    if not email:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')

    if not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for single_user in users:
        if not single_user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    user = users[0]
    session_id = auth.create_session(user.id)
    session_name = getenv("SESSION_NAME")
    res = jsonify(user.to_json())
    res.set_cookie(session_name, session_id)
    return res


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def logout():
    '''deletes session id passed as cookie'''
    from api.v1.app import auth
    status = auth.destroy_session(request)

    if not status:
        abort(404)

    return jsonify({}), 200
