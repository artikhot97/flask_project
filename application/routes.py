
# from datetime import datetime as dt
# from flask import current_app as app
# from .models import db, User

# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, session, url_for,make_response
# )


# bp = Blueprint('auth', __name__, url_prefix='/auth')


# @bp.route('/')
# def user_records():
#     """Create a user via query string parameters."""
#     username = request.args.get('user')
#     email = request.args.get('email')
#     if username and email:
#         new_user = User(
#             username=username,
#             email=email,
#             created=dt.now(),
#             admin=False
#         )
#         db.session.add(new_user)  # Adds new User record to database
#         db.session.commit()  # Commits all changes
#     return make_response(f"{new_user} successfully created!")


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=9000)