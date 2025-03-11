import pyodbc
from flask_restful import Resource
from app.utils.db import get_db_connection
import datetime
class TestConnection(Resource):
    def get(self):
        connection = None
        cursor = None
        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tb_Users")
            columns = [column[0] for column in cursor.description]
            results = []
            for row in cursor.fetchall():
                row_dict = dict(zip(columns, row))
                # Convert datetime objects to string using isoformat()
                for key, value in row_dict.items():
                    if isinstance(value, datetime.datetime):
                        row_dict[key] = value.isoformat()
                results.append(row_dict)
            return {'data': results}, 200
        except pyodbc.Error as e:
            return {'error': str(e)}, 500
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()