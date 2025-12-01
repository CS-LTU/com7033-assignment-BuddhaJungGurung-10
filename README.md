# Secure web application for local hospital to manage patient stroke records using Flask, MongoDB, and SQLAlchemy.

## Overview

This assignment is a Flask based web application developed to help local hospital manage patient stroke records securly and efficiently. It uses SQlite for user authentication and MongoDB for storing patient stroke records.

## Features
The key features of the applixation are:
- User Registration and Authentication
- Add, View, Update, and Delete Patient Stroke Records
- Secure Password Hashing
- Form Validation
- Responsive UI with Bootstrap
- Flash Messages for User Feedback
- Role-Based Access Control


## Technologies Used
- Flask
- Flask-WTF
- Flask-Login
- Flask-SQLAlchemy
- Flask-PyMongo
- Bootstrap
- SQLite
- MongoDB
- Pytest


## Project Structure
The project is created following flask best practices described in official flask documentation with a modular structure(application factory pattern). It is organized as follows:
- **app** : It contains the main application package with sub-packages(auth, home, templates, config, logging, etc.).
- **dataset** : It contains the stroke prediction dataset used for testing.
- **scripts** : This folder conntain two scripts responsible for creating syste admin and loading initial data to mongodb.
- **tests** : It contains unit tests for the application.
- **.example.env** : Example environment variables file.
- **.gitignore** : Git ignore file.
- **pytest.ini** : Pytest configuration file.
- **README.md** : Project documentation file.
- **requirements.txt** : List of project dependencies.
- **wsgi.py** : Entry point for the application.


## Working Flow
 First environment is setup and dependencies are installed. Then using scripts in the script folder, dataset is loaded to mongodb, and a system admin is created. System admin then login in with the credentials provided during creation. After successful login, admin can go to admin dashboard and create other users(doctors and nurses). These user can then login and manage patient stroke records.

 ## Implemented Security Measures
 - **Environment Variables** : All the sensetive information like secret keys and database URIs are stored in environment variables.
 - **Session Management** : Flask-Login is used to manage user sessions securely.
 - **Password Hashing** : Passwords are hashed using Werkzeug's security module before storing them in the database.
 - **CSRF Protection** : Flask-WTF are enabled on all form to protect against CSRF attacks.
- **Input Validation** : WTForms validators are used to ensure that user inputs are valid and safe.
- **XSS Protection** :  Jinja2 template is used that auto-escapes user inputs to prevent XSS attacks.
- **Error Handling and Logging** : 
    - Custom error pages are created for common HTTP errors like 404 and 500.
    - Logging is implemented to keep track of important events and errors (sensetive information is not logged).
- **Pagination** : Pagination concept using skip and limit is implemented to prevent performance issues as the dataset has hign number of records and displaing all records at once leads to slow response times.


## Setup Instructions
1. Clone the repository to your local machine.
2. Create a virtual environment and activate it.
```bash
python -m venv .venv
# for windows
.venv\Scripts\activate

# for mac/linux
source .venv/bin/activate
```
3. Install the required dependencies.
```bash
pip install -r requirements.txt
```
4. Create a `.env` file in the root directory and add the necessary environment variables as shown in `.example.env`.
Aslo defalut values are provided in config.py file in case environment variables are not set.
5. Run the scripts in the `scripts` folder to create a system admin and load initial data to MongoDB.
```bash
# create system admin
python scripts/create_sys_admin.py

# load initial data to mongodb
python scripts/load_records.py
```
6. Start the Flask application.
```bash
python wsgi.py
```
7. Open this URL in your web browser:
```
http://localhost:5000
```

## Testing
To run the unit tests for the application, use the following command:
```bash
pytest
```

## Use of AI
This assignment used generative AI in the following ways for the purposes of completing the assignment more efficiently:
- `Research` : unserstanding best practice for secure web application developement with flask.
- `Feedback and suggestions` :  checked for implemented approach and suggestions for improvement.
- `Editing` : reviewing readme file for better readiability and structure.

## Tools Used
- ChatGPT - for code review, understanding concepts, and reviewing documentation.


# Helpful Resourses.
1. Flask Documentation:
    - Understanding Flask and its extensions.
    - Flask tutorials for implementing application factory pattern with flask project structure.
2. MongoDB Documentation:
    - Learning how to interact with MongoDB using Flask-PyMongo.


