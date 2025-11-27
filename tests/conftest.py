import pytest
from app import create_app, db
from app.extensions import mongo
from werkzeug.security import generate_password_hash
import mongomock
from app.models import User

@pytest.fixture(scope="function")
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "MONGO_URI": "mongodb://localhost:27017/test_db",
        "WTF_CSRF_ENABLED": False,
        "LOGIN_DISABLED": False,
    })

  

    mongo.cx = mongomock.MongoClient()
    mongo.db = mongo.cx["test_db"]

    with app.app_context():

        db.drop_all()
        db.create_all()

        admin_user = User(
            username="admin",
            email="admin@gmail.com",
            role="admin"
        )
        admin_user.set_password("asd123asd")

        doctor_user = User(
            username="doctor",
            email="doctor@gmail.com",
            role="doctor"
        )
        doctor_user.set_password("doctorpass")

        db.session.add(admin_user)
        db.session.add(doctor_user)

        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@ pytest.fixture()
def client(app):
    return app.test_client()
