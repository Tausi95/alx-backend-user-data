#!/usr/bin/env python3
"""
Main flask app
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """Welcome message"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users', methods=['POST'], strict_slashes=False)
def reg_user():
    """Register a new User"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> dict:
    """Login user"""
    email = request.form.get('email')
    password = request.form.get('password')
    valid_login = AUTH.valid_login(email, password)
    if valid_login:
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout user"""
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect(url_for('welcome'))
    else:
        abort(403)


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Get user profile from session_id cooke
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        abort(403)


@app.route('/reset_password', methods=['POST', 'PUT'], strict_slashes=False)
def get_reset_password_token():
    """Get reset password token"""
    email = request.form.get('email')
    if request.method == 'POST':
        try:
            token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": token}), 200
        except ValueError:
            abort(403)

    if request.method == 'PUT':
        token = request.form.get('reset_token')
        new_password = request.form.get('new_password')
        try:
            AUTH.update_password(token, new_password)
            return jsonify({"email": email,
                            "message": "Password updated"}), 200
        except ValueError:
            abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
