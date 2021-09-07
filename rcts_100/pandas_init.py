import pandas as pd


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
        self.df = pd.DataFrame(self.dataset)

    def add_data(self, logdate, logtime, username, url, caption, dateposted, taggedaccounts):
        self.log_date.append(logdate)
        self.log_time.append(logtime)
        self.username.append(username)
        self.url.append(url)
        self.caption.append(caption)
        self.date_posted.append(dateposted)
        self.tagged_accounts.append(taggedaccounts)

    def create_excel(self):
        self.df.to_excel(self.filename)

    def read_excel(self):
        reee = pd.read_excel(self.filename, engine="openpyxl")
        return reee


if __name__ == '__main__':
    test = Event("testing.xlsx")
    print(test.excelread)
