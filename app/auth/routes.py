# this file contains the code logic to handle user registration, login, logout and user management. 


from flask import render_template, redirect, session, url_for, flash, request, sessions
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegisterForm, LoginForm
from ..models import User
from ..extensions import db, login_manager
from . import bp
from urllib.parse import urlparse as url_parse


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#  creating login url route
@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home.index"))
    
    login_form = LoginForm()

    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()

        # if not user:
        #     user = User.query.filter_by(username=login_form.email.data).first()


        if user and user.check_password(login_form.password.data):
            login_user(user)
            next_page = request.args.get("next")

            if not next_page or url_parse(next_page).netloc != "":
                next_page = url_for("home.index")
            flash("Welcome to Stroke Record Manager.", "success")
            return redirect(next_page)

        flash("Incorrect email or password.", "danger")


    return render_template("auth/login.html", form=login_form)


#  register part
@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated and current_user.role != "admin":
        flash("Only admin users can register new users.", "danger")
        return redirect(url_for("home.index"))
    
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        # checking if user already exists 
        existing_user = User.query.filter(
            (User.email == register_form.email.data) | (User.username == register_form.username.data)
        ).first()

        if existing_user:
            flash("User with this email or username already exists.", "danger")
            return redirect(url_for("home.admin_dashboard"))
        try:

            new_user = User(
                username=register_form.username.data,
                email=register_form.email.data,
                role=register_form.role.data,
            )
            new_user.set_password(register_form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("User Registration successful!", "success")
        except Exception as e:
            db.session.rollback()
            flash("Error occured : " + str(e), "danger")

        else:
            flash("User Registration successful!", "success")
    else:
        if register_form.errors:
            for field, errors in register_form.errors.items():
                for error in errors:
                    flash(f"Error in {field}: {error}", "danger")
    
    return redirect(url_for("home.admin_dashboard"))

   

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))



# feature to delete user by admin   
@bp.route("/delete-user/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if current_user.role != "admin":
        flash("You donot have permission to delete users.", "danger")
        return redirect(url_for("home.admin_dashboard"))
    
    user = User.query.get_or_404(user_id)

    if user.role == "admin":
        flash("Admin users cannot be deleted.", "danger")
        return redirect(url_for("home.admin_dashboard"))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully.", "success")
        print("User deleted successfully.") # Debug print statement to verify deletion
        return redirect(url_for("home.admin_dashboard"))
    except Exception as e:
        db.session.rollback()
        flash("Error deleting user: " + str(e), "danger")
        return redirect(url_for("home.admin_dashboard"))
