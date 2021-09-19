import sys
from typing import Type
from DatabaseClass import DatabaseClass
from requests_html import HTMLSession
from Mail import Mail
import wget
import os


def main():
    db = DatabaseClass()
    mail = Mail()
    text = sys.argv[1]
    date = ' '.join(text.split()[1:3])
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
            mail.send_mail(files)
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


if __name__ == "__main__":
    main()
