from django.db import connection


class Book:
    def __init__(self, id=None, title=None, author=None, genre=None):
        self.id = id
        self.title = title
        self.author = author
        self.genre = genre

    @staticmethod
    def get_dict(id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM books WHERE id = %s", [id])
            row = cursor.fetchone()
            return {"id": row[0], "title": row[1], "author": row[2], "genre": row[3]}

    @staticmethod
    def list(condition: dict = "", user_id=None):
        if condition:

            condition = " WHERE " + " AND ".join(
                f"{str(key)} LIKE '{item[0]}'" for key, item in condition.items()
            )
        query = f"""
            SELECT b.*, r.rating FROM books b
            LEFT JOIN
                reviews r
                ON b.id = r.book_id AND r.user_id = {user_id}
            {condition}
            ORDER BY title;
            """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
            return data

    def __str__(self):
        return self.title
