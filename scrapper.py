import pydantic
import sys
from DatabaseClass import DatabaseClass


def main():
   # print ('Number of arguments:', len(sys.argv), 'arguments.')
   # print ('Argument List:', sys.argv[1])
    db = DatabaseClass()
    text = sys.argv[1]
    date = ' '.join(text.split()[1:3])
    select = db.fetchone("SELECT * FROM ostatnia_aktualizacja")
    print(select)
    print(date)


if __name__ == "__main__":
    main()

print("Guru99")
