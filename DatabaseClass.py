import sqlite3


class DatabaseClass:
    def __init__(self) -> None:
        self.con = sqlite3.connect('dane.db')

    def fetchone(self, val):
        cursor = self.con.cursor()
        cursor.execute(val)
        self.con.commit()
        result = cursor.fetchone()
        cursor.close()
        return result

