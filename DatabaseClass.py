import sqlite3


class DatabaseClass:
    def __init__(self) -> None:
        self.con = sqlite3.connect('dane.db')
        self.cursor = self.con.cursor()

    def get_row(self, val: str):
        try:
            self.cursor.execute(val)
            self.con.commit()
            return self.cursor.fetchone()
        except Exception as e:
            print(e)

    def get_rows(self, val: str):
        try:
            self.cursor.execute(val)
            self.con.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def query(self, val: str):
        try:
            self.cursor.execute(val)
            self.con.commit()
        except Exception as e:
            print(e)

    def close(self):
        print("Close database")
        self.cursor.close()
        self.con.close()

