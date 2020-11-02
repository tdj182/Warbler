"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

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

        u = User.signup("testuser","test@test.com","HASHED_PASSWORD", None)

        db.session.add(u)
        db.session.commit()

        self.u = u

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_new_message(self):
        """New message test"""

        m=Message(text="test", user_id=self.u.id)

        db.session.add(m)
        db.session.commit()

        # check for only one message with 'test' as the text
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "test")

