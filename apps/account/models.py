from django.db import connection


class User:
    def __init__(self, id=None, username=None, password=None):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get_by_username(username):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", [username])
            row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], password=row[2])
            return None

    @staticmethod
    def get(user_id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
            row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], password=row[2])
            return None
