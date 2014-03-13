# coding=utf-8
from flask import json, jsonify
import cipher

__author__ = 'Linus'

import os, unittest, routes, database, tempfile

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, routes.app.config['DATABASE'] = tempfile.mkstemp()
        routes.app.config['TESTING'] = True
        self.app = routes.app.test_client()
        self.db = database.init(routes.app)

    def tearDown(self):
        os.close(self.db_fd)

    def test_get_group(self):
        with routes.app.test_request_context():
            database.create_new_group("Sweden", "vip")

            # JSON Object we expect to get back
            json_test = json.loads("""{ "groups": [
                {
                    "id": 1,
                    "name": "Sweden",
                    "priority": "vip"
                }
            ]}""")

            # Test get_groups(group_name)
            rv = self.app.get('/api/v1.0/groups')  # JSON Object we get back
            self.assertEquals(json.loads(rv.data), json_test)

    def test_invalid_group_name(self):
        with routes.app.test_request_context():
            # Invalid group name during group creation
            try:
                database.create_new_group("Invalid Name", "low")
                self.assertTrue(0)  # Gives assertion error if the above function fails
            except SyntaxError:
                self.assertTrue(1)  # SyntaxError got raised, as wanted.

            # Invalid group name during adding member
            try:
                database.add_group_members("Invalid Name", "low")
                self.assertTrue(0)  # Gives assertion error if the above function fails
            except SyntaxError:
                self.assertTrue(1)  # SyntaxError got raised, as wanted.


    def test_get_group_members(self):
        with routes.app.test_request_context():
            database.create_new_group("GroupWithMembers", "low")

            database.add_registered_user(["Linus", "Kortesalmi", "linus.kortesalmi@mail.com",
                                          "Sweden", "Linkpping", "g_plus"])

            database.add_group_members("GroupWithMembers", [0, 1])

            # JSON Object we expect to get back
            json_test = json.loads("""{ "members": [
                {
                    "answered": "FALSE",
                    "email": "linus.kortesalmi@mail.com",
                    "id": 1,
                    "name": "Linus Kortesalmi"
                }
            ]}""")

            rv = self.app.get('/api/v1.0/groups/GroupWithMembers')  # JSON Object we get back
            self.assertEquals(json.loads(rv.data), json_test)

    def test_get_persons_and_ids(self):
         with routes.app.test_request_context():
            database.add_registered_user(["Linus", "Kortesalmi", "linus.kortesalmi@mail.com",
                                          "Sweden", "Linkpping", "g_plus"])
            expected_answer = [{'id': 1, 'name': u'Linus Kortesalmi'}]

            self.assertEquals(database.get_persons_and_ids(), expected_answer)

    def test_get_signups(self):
         with routes.app.test_request_context():
            database.add_registered_user(["Linus", "Kortesalmi", "linus.kortesalmi@mail.com",
                                          "Sweden", "Linkoping", "g_plus"])
            expected_answer = [{'city': u'Linkoping', 'country': u'Sweden', 'name': u'Linus Kortesalmi',
                                'reference': u'g_plus', 'email': u'linus.kortesalmi@mail.com'}]

            self.assertEquals(database.get_signups(), expected_answer)

    def test_get_signup_count(self):
        with routes.app.test_request_context():
            database.add_registered_user(["Linus", "Kortesalmi", "linus.kortesalmi@mail.com",
                                          "Sweden", "Linkoping", "g_plus"])
            expected_answer = 1

            self.assertEquals(database.get_signup_count(), expected_answer)

if __name__ == '__main__':
    unittest.main()