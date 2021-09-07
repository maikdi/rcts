import mysql.connector
import pandas as pd
from datetime import date
import time


class DatabaseConnection:
    def __init__(self):
        self.mydb = mysql.connector.connect(host="127.0.0.1",
                                            user="root",
                                            password="jmilliaan03")
        self.c = self.mydb.cursor()

    def exec(self, query):
        self.c.execute(query)

    def printcursor(self):
        self.a = self.c.fetchall()
        for i in self.a:
            print(i)

    def commit(self):
        self.mydb.commit()

    def log(self, database, table, username, url, caption, postdate, tagged_account):
        self.exec(f"USE {database}")
        today = str(date.today().strftime('%Y-%m-%d'))
        now = str(time.strftime("%H:%M:%S"))
        self.exec(
            f"INSERT INTO {table}"
            f"(log_date, log_time, username, url, caption, date_posted, tagged) "
            f"VALUES('{today}', '{now}', '{username}', "
            f"'{url}', '{caption}', '{postdate}', "
            f"'{tagged_account}')")
        self.commit()


class Acquisition(DatabaseConnection):
    def __init__(self):
        super(Acquisition, self).__init__()
        self.number = 0
        self.log_date = ""
        self.username = ""
        self.url = ""
        self.caption = ""

    def get_row(self):
        self.exec("SELECT")


class Event:
    def __init__(self, filename):
        self.number = []
        self.log_date = []
        self.log_time = []
        self.username = []
        self.url = []
        self.caption = []
        self.date_posted = []
        self.tagged_accounts = []
        self.filename = filename
        self.excelread = self.read_excel()
        self.dataset = {"Log Date": self.log_date,
                        "Username": self.username,
                        "URL": self.url,
                        "Caption": self.caption,
                        "Date Posted": self.date_posted,
                        "Tagged Accounts": self.tagged_accounts}

    def add_data(self, username, url, caption, dateposted, taggedaccounts):
        today = str(date.today().strftime('%Y-%m-%d'))
        now = str(time.strftime("%H:%M:%S"))
        self.log_date.append(today)
        self.log_time.append(now)
        self.username.append(username)
        self.url.append(url)
        self.caption.append(caption)
        self.date_posted.append(dateposted)
        self.tagged_accounts.append(taggedaccounts)

    def create_excel(self):
        self.df = pd.DataFrame(self.dataset)
        self.df.to_excel(self.filename)

    def read_excel(self):
        reee = pd.read_excel(self.filename, engine="openpyxl")
        return reee
