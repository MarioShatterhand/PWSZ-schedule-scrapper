import sqlite3


class DatabaseClass:
    def __init__(self) -> None:
        self.con = sqlite3.connect('dane.db')
        print("Init innit?!")

    def fetchone(self, val: str):
        try:
            print("Here it is")
            print(val)
            cursor = self.con.cursor()
            cursor.execute("SELECT * FROM ostatnia_aktualizacja")
            self.con.commit()
            print(cursor.fetchall())
            result = cursor.fetchone()
           # cursor.close()
        except Exception as e:
            print(e)
        return result

