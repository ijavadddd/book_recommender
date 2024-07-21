from collections import defaultdict
from django.db import connection


class Recommendation:

    @staticmethod
    def rated_genre_average(user_id):
        query = f"""SELECT b.genre, r.rating FROM books b
                    LEFT JOIN reviews r 
                    ON b.id = r.book_id AND r.user_id = {user_id}
                    WHERE r.rating IS NOT NULL
                    ORDER BY r.rating;
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
            genre_ratings = defaultdict(list)
            for entry in data:
                genre_ratings[entry['genre']].append(entry['rating'])

            # Calculate average rating for each genre
            genre_averages = [
                {'genre': genre, 'average_rating': sum(ratings) / len(ratings)}
                for genre, ratings in genre_ratings.items()
            ]
            return sorted(genre_averages, key=lambda x: x['average_rating'], reverse=True)

    @classmethod
    def suggest_genre(cls, user_id):
        genres = cls.rated_genre_average(user_id)
        if not genres:
            return None
        genres_title = ", ".join("'{0}'".format(item["genre"]) for item in genres)
        # Create a CASE statement for custom sorting
        case_statement = ' '.join(
            "WHEN genre = '{0}' THEN {1}".format(item["genre"], index + 1)
            for index, item in enumerate(genres)
        )
        order_by_clause = f"ORDER BY CASE {case_statement} ELSE {len(genres) + 1} END, r.rating"

        query = f"""SELECT b.*, r.rating FROM books b
                    LEFT JOIN reviews r 
                    ON b.id = r.book_id AND r.user_id = {user_id}
                    WHERE r.rating IS NULL AND
                    genre IN ({genres_title})
                    {order_by_clause};
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
            return data
