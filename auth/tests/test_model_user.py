from unittest import TestCase

from auth.models import Users, User


class TestUser(TestCase):

    def test_empty_construction(self):
        self.assertRaises(TypeError, lambda: User())

    def test_one_arg_construction(self):
        self.assertRaises(TypeError, lambda: User(idx=1))

    def test_two_args_construction(self):
        self.assertRaises(TypeError, lambda: User(idx=1, name="kate"))

    def test_correct_construction(self):
        User(idx=1, name="kate", email="email")


class TestUsers(TestCase):

    def setUp(self) -> None:
        self.users = Users()
        self.user = User(1, "kate", "email")

    def test_construction(self):
        Users()

    def test_add_user_not_User_class(self):
        user = "kate"
        self.assertFalse(self.users.add_user(user))

    def test_add_user_User_class(self):
        self.assertTrue(self.users.add_user(self.user))

    def test_get_user_incorrect_id(self):
        self.assertEqual(None, self.users.get_user(2))

    def test_get_user_correct_id(self):
        self.users.add_user(self.user)
        self.assertEqual(self.user, self.users.get_user(1))

    def test_remove_user_incorrect_id(self):
        test = Users()
        test.add_user(self.user)
        remove = Users()
        remove.add_user(self.user)
        remove.remove_user(2)
        self.assertEqual(test.users, remove.users)

    def test_remove_user_correct_id(self):
        test = Users()
        test.add_user(self.user)
        remove = Users()
        remove.add_user(self.user)
        remove.remove_user(1)
        self.assertNotEqual(test.users, remove.users)
