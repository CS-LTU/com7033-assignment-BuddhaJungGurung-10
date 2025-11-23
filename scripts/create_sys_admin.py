"""
CLI script to create a system administrator user.
"""
import os
import sys
from getpass import getpass

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User
from sqlalchemy.exc import IntegrityError



def main():
    """Function to create a sys admin user via CLI."""
    app = create_app()
    app.app_context().push()

    if User.query.filter_by(role="admin").first():
        print("An admin user already exists. Exiting.")
        return
    
    print("Create System Administrator Account")
    email = input("Email: ").strip()
    username = input("Username: ").strip()

    password = getpass("Password: ")
    confirm_password = getpass("Confirm Password: ")

    if password != confirm_password:
        print("Passwords do not match. Exiting.")
        return

    sys_admin = User( 
        username=username,
        email=email,
        role="admin",
    )
    sys_admin.set_password(password)

    db.session.add(sys_admin)
    try:
        db.session.commit()
        print("System administrator account created successfully.")
    except IntegrityError:
        db.session.rollback()
        print("Error: Email or username already exists. Exiting.")


if __name__ == "__main__":
    main()