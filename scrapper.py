import pydantic
import sys
from DatabaseClass import DatabaseClass


def main():
   # print ('Number of arguments:', len(sys.argv), 'arguments.')
   # print ('Argument List:', sys.argv[1])
    db = DatabaseClass()
    text = sys.argv[1]
    date = ' '.join(text.split()[1:3])
    try:
        select = db.fetchone(f"SELECT data_godzina FROM ostatnia_aktualizacja WHERE data_godzina == {date}")
        if select is None:
            db.query(f"INSERT INTO ostatnia_aktualizacja VALUES(?, {date})")
    except Exception as e:
        print(e)
    print("Select: ", select)


if __name__ == "__main__":
    main()

print("Guru99")
