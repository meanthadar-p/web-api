import sqlite3


class ConnectDatabase:
    def __init__(self):
        pass

    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error as e:
            print(e)

        return conn

    @classmethod
    def execute_query(cls, db_file, query, to_filter=[]):
        conn = cls.create_connection(db_file)
        cur = conn.cursor()
        results = cur.execute(query, to_filter).fetchall()
        return results

    # SELECT * FROM <table> WHERE <cond>
    # UPDATE <table> SET column1 = v1, column2 = v2 WHERE <cond>
    # INSERT INTO <table> VALUES ('1018','1', '1');
    # DELETE FROM <table> WHERE <cond>
