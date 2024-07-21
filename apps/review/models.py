from django.db import connection


class Review:
    def __init__(self, id=None, book_id=None, user_id=None, rating=None):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.rating = rating

    @staticmethod
    def get_dict(id):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM reviews WHERE id = %s", [id])
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            data = dict(zip(columns, row))
            return data

    @staticmethod
    def count(condition_dict: dict):
        condition = " WHERE " + " AND ".join(
            f"{str(key)} = {str(item)}" for key, item in condition_dict.items()
        )
        query = f"SELECT COUNT(*) FROM reviews {condition};"

        with connection.cursor() as cursor:
            cursor.execute(query, [condition])
            count = cursor.fetchone()
            return count[0]

    @staticmethod
    def create(value_dict: dict, user_id=None):
        columns = ", ".join(f"{str(key)}" for key in value_dict.keys())
        values = ", ".join(f"{str(value)}" for value in value_dict.values())
        query = f"""
                WITH inserted_review AS (
                    INSERT INTO reviews ({columns})
                    VALUES ({values})
                    ON CONFLICT DO NOTHING
                    RETURNING *
                )
                SELECT
                    b.*,      
                  b.id AS book_id,
                  ir.rating AS rating 
                FROM
                    books b
                LEFT JOIN
                    inserted_review ir
                    ON b.id = ir.book_id
                WHERE b.id = ir.book_id;
                """
        with connection.cursor() as cursor:
            cursor.execute(query)
            instance = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            data = dict(zip(columns, instance))
            return data

    @staticmethod
    def update(update_dict, condition_dict: dict):
        condition = " WHERE " + " AND ".join(
            f"{str(key)} = {str(item)}" for key, item in condition_dict.items()
        )
        values = " AND ".join(
            f"{str(key)} = {str(item)}" for key, item in update_dict.items()
        )
        query = f"UPDATE reviews SET {values} {condition} RETURNING *;"

        with connection.cursor() as cursor:
            cursor.execute(query)
            instance = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            data = dict(zip(columns, instance))
            return data

    @staticmethod
    def delete(condition_dict: dict):
        try:
            condition = " WHERE " + " AND ".join(
                f"{str(key)} = {str(item)}" for key, item in condition_dict.items()
            )
            query = f"DELETE FROM reviews {condition};"

            with connection.cursor() as cursor:
                cursor.execute(query)
                return True
        except:
            return None

    def __str__(self):
        return self.book_id
