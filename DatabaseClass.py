import sqlite3


class DatabaseClass:
    def __init__(self) -> None:
        self.con = sqlite3.connect('dane.db')

    def fetchone(self, val: str):
        try:
            cursor = self.con.cursor()
            cursor.execute(val)
            self.con.commit()
            return cursor.fetchone()
        except Exception as e:
            print(e)

    def query(self, val: str):
        try:
            cursor = self.con.cursor()
            cursor.execute(val)
            self.con.commit()
        except Exception as e:
            print(e)

