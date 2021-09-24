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



def main():
    db = DatabaseClass()
    mail = Mail()
    date_struct = re.compile("\d\d\d\d-\d\d-\d\d \d\d:\d\d")
    command = 'curl --silent https://pwsztar.edu.pl/instytut-politechniczny/informatyka/harmonogramy/'
    ret = subprocess.run(command, capture_output=True, shell=True)
    text = ret.stdout.decode('UTF-8')
    reg = date_struct.findall(text)
    date = reg[1]
    #date = ' '.join(text.split()[1:3])
    files = []
    try:
        try:
            select = db.get_row(
                f"SELECT data_godzina FROM ostatnia_aktualizacja WHERE data_godzina == '{date}'")[0]
        except TypeError:
            select = None
        if select is None:
            s = HTMLSession()
            r = s.get(
                "https://pwsztar.edu.pl/instytut-politechniczny/informatyka/harmonogramy/")

            sel = '#rozmCZ > ul:nth-child(5) > li:nth-child(3) > ul > li'

            schedules = r.html.find(sel)

            for schedule in schedules:
                if schedule.full_text == "Informatyka w telekomunikacji" or schedule.full_text == "Informatyka w Telekomunikacji" or schedule.full_text == "Systemy teleinformatyczne" or schedule.full_text == "Systemy Teleinformatyczne":
                    links = schedule.links
                    for link in links:
                        filename = f"{schedule.full_text}.pdf"
                        wget.download(link, out=filename)
                        files.append(filename)

            sel = '#rozmCZ > ul:nth-child(7) > li:nth-child(3) > ul > li'

            groups = r.html.find(sel)

            for group in groups:
                if group.full_text == "Systemy teleinformatyczne" or group.full_text == "Systemy Teleinformatyczne":
                    links = group.links
                    for link in links:
                        filename = f"{group.full_text}.pdf"
                        wget.download(link, out=filename)
                        files.append(filename)
            for file in files:
                m = hash_file(file)
                print(m)
            mail.send_mail(files, date)
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
   with open(filename,'rb') as file:

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
