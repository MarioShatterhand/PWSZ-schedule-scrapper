import sys
from typing import Type
from DatabaseClass import DatabaseClass
from requests_html import HTMLSession
from Mail import Mail
import wget
import os
import subprocess
import re
import hashlib
import datetime


def main():
    now = datetime.datetime.now()
    print("\n Wykonano: ", (str(now)))
    db = DatabaseClass()
    mail = Mail()
    date_struct = re.compile("\d\d\d\d-\d\d-\d\d \d\d:\d\d")
    command = 'curl --silent https://pwsztar.edu.pl/instytut-politechniczny/informatyka/harmonogramy/'
    ret = subprocess.run(command, capture_output=True, shell=True)
    text = ret.stdout.decode('UTF-8')
    reg = date_struct.findall(text)
    if len(reg) == 0:
        date_struct = re.compile("\d\d\d\d-\d\d-\d\d \d:\d\d")
        reg = date_struct.findall(text)
    date = reg[0]
    print(date)
    #date = ' '.join(text.split()[1:3])
    files = []
    users = []
    sendfile = []
    try:
        users = db.get_rows("SELECT * FROM studenci")
        print(users)
        
        try:
            select = db.get_row(
                f"SELECT data_godzina FROM ostatnia_aktualizacja WHERE data_godzina == '{date}'")[0]
            print("Odpowiedź na zapytanie SELECT: ", select, " \n Jeżeli widzisz tą wiadomość, to bot nie pobrał plików, ponieważ znalazł datę aktualizacji w bazie danych")
        except TypeError:
            select = None
        if select is None:
            print("Rozpoczęto pobieranie plików")
            s = HTMLSession()
            r = s.get(
                "https://pwsztar.edu.pl/instytut-politechniczny/informatyka/harmonogramy/")
            sel = '#rozmCZ > ul:nth-child(5)'
            schedules = r.html.find(sel)
            print(schedules)
            for schedule in schedules:
                print(schedule)
                links = schedule.links
                for link in links:
                    filename = link[50:]
                    if filename[:3] == "wsz":
                        filename = filename[::-1]
                        filename = filename + "p"
                        filename = filename[::-1]
                        print("DODANE P: ", filename)
                    wget.download(link, out=filename)
                    # print("CZĘŚĆ: ", filename[38:-4])
                    files.append(filename)

            sel = '#rozmCZ > ul:nth-child(7)'
            groups = r.html.find(sel)
            print(groups)
            for group in groups:
                print(group)
                links = group.links
                for link in links:
                    filename = link[50:]
                    if filename[:3] == "wsz":
                        filename = filename[::-1]
                        filename = filename + "p"
                        filename = filename[::-1]
                        print("DODANE P: ", filename)
                    wget.download(link, out=filename)
                    # print("CZĘŚĆ: ", filename[39:-4])
                    files.append(filename)

            for file in files[:]:
                m = hash_file(file)
                try:
                    select = db.get_row(
                        f"SELECT nazwa FROM pliki WHERE sha == '{m}'")[0]
                    print("File removed from sending list: ", select)
                    if os.path.exists(select):
                        os.remove(select)
                    else:
                        print("Can not delete the file as it doesn't exists")
                    files.remove(select)
                except TypeError:
                    select = None
                if select is None:
                    db.query(f"INSERT INTO pliki VALUES('{m}', '{file}')")

            for user in users:
                print(user)
                for file in files:
                    # print("FILE: ", file[38:-4], " USER: ", user[1])
                    if str(user[1]) == file[38:-4] or str(user[1]) == file[39:-4]:
                        sendfile.append(file)
                        print("Pierwszy ", user[0])

                    if user[2] != "" and user[2] in file[38:-4] or user[2] in file[39:-4]:
                        sendfile.append(file)
                        print("Drugi ", user[0]) 
                mail.send_mail(sendfile, date, user[0])
                sendfile = []

            
            db.query(
                f"INSERT INTO ostatnia_aktualizacja (data_godzina) VALUES('{date}');")

        for file in files:
            if os.path.exists(file):
                os.remove(file)
            else:
                print("Can not delete the file as it doesn't exists")
    except Exception as e:
        print(e)
    db.close()


def hash_file(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:

        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


if __name__ == "__main__":
    main()
