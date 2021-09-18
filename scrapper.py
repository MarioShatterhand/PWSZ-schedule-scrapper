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
        select = db.get_row(f"SELECT data_godzina FROM ostatnia_aktualizacja WHERE data_godzina == '{date}'")[0]
        if select is None:
            print("Hmm?")
            db.query(f"INSERT INTO ostatnia_aktualizacja (data_godzina) VALUES('{date}');")
    except Exception as e:
        print(e)
    db.close()
    print("Select: ", select)


if __name__ == "__main__":
    main()

print("Guru99")
