#!/usr/bin/env python3
"""
View for all authenitcated sessions"""
from api.v1.views import app_views
from flask import jsonify, request, abort
import os
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def auth_session_login():
    """Handles session login"""
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        return jsonify({'error': 'email missing'}), 400

    if password is None:
        return jsonify({'error': 'password missing'}), 400

    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({'error': 'no user found for this email'}), 404
    user = users[0]
    if user.is_valid_password(password):
        from api.v1.app import auth
        session_id = auth.create_session(user.id)
        response = jsonify(user.to_json())
        cookie_name = os.getenv('SESSION_NAME')
        response.set_cookie(cookie_name, session_id)
        return response

    return jsonify({'error': 'wrong password'}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def auth_session_logout():
    """Handles session logout"""
    from api.v1.app import auth
    if auth.destroy_session(request) is False:
        abort(404)
    return jsonify({}), 200
