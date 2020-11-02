"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from sqlalchemy import exc

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        
        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        u1 = User.signup("testuser1","test1@test.com","HASHED_PASSWORD", None)
        u2 = User.signup("testuser2","test2@test.com","HASHED_PASSWORD", None)

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.u1 = u1
        self.u2 = u2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""
        print('user model')

        u = User.signup("testuser","test@test.com","HASHED_PASSWORD", None)

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

        # Deleting the user should result in the two setup users
        db.session.delete(u)
        db.session.commit()
        users = User.query.all()
        self.assertEqual(len(users), 2)

    def test_following(self):
        """Test"""

        # First, the users should not be followed/following
        self.assertEqual(False, User.is_following(self.u1, self.u2))
        self.assertEqual(False, User.is_followed_by(self.u2, self.u1))

        self.u1.following.append(self.u2)
        db.session.commit()
        # User 1 should now be following User 2
        self.assertEqual(True, User.is_following(self.u1, self.u2))
        self.assertEqual(True, User.is_followed_by(self.u2, self.u1))

    def test_invalid_username_signup(self):
        User.signup(None, "test@test.com", "password", None)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
            
    def test_email_username_signup(self):
        User.signup('test', None, "password", None)
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


    def test_authentication(self):
        signup_user = User.signup("testuser","test@test.com","HASHED_PASSWORD", None)
        db.session.commit()
        login_user = User.authenticate(signup_user.username, "HASHED_PASSWORD")
        
        self.assertEqual(login_user.id, signup_user.id)

    def test_wrong_username(self):
        self.assertFalse(User.authenticate("somefakeuser", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))