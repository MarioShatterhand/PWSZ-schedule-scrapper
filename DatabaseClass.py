import sqlite3


class DatabaseClass:
    def __init__(self) -> None:
        self.con = sqlite3.connect('dane.db')

    def fetchone(self, val: str):
        try:
            cursor = self.con.cursor()
            cursor.execute(val)
            self.con.commit()
            # print(cursor.fetchall())
            return cursor.fetchone()
           # cursor.close()
        except Exception as e:
            print(e)

