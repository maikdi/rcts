import requests
import html
import json
import pandas as pd


class URLFile:
    def __init__(self, location):
        self.location = location
        self.df = pd.read_excel(self.location,
                                sheet_name="Sheet1", engine="openpyxl")
        self.url_list = self.df_to_list()
        self.size = len(self.url_list)
        print(f"IG posts from {location}\nAcquiring {self.size} posts")

    def df_to_list(self):
        urllist = []
        for i in self.df['url']:
            urllist.append(i)
        return urllist


class InstagramData:
    def __init__(self, url):
        self.added_text = "?__a=1"
        self.months = ["January", "February", "March",
                       "April", "May", "June",
                       "July", "August", "September",
                       "October", "November", "December"]

        self.post_url = url
        self.html_url = self.post_url + self.added_text

        self.header = {'User-Agent': "Mozilla/5.0 "
                                     "(Windows NT 10.0; Win64; x64) "
                                     "AppleWebKit/537.36 "
                                     "(KHTML, like Gecko) "
                                     "Chrome/93.0.4577.63 "
                                     "Safari/537.36",
                       "cookie": "ig_did=EEC95D6A-0846-47F2-8B87-53F3B64A6007;"
                                 "ig_nrcb=1;"
                                 "mid=YT7mCwALAAEdoraS5_1uT4cn27bC;"
                                 "csrftoken=NS203ubZI10YdeBCQKzAhUgtV0jHIl2G;"
                                 "ds_user_id=49129421296; sessionid=49129421296:KbpWG3Hs1XyaFX:3;"
                                 "rur='VLL\05449129421296"
                                 "\0541663049728:"
                                 "01f750f0a8333fccbaf70dce2a591218e4cf26da10754085228a1aedeafdd501b8e69418'"}

        self.request_text = requests.get(self.html_url, headers=self.header)
        self.statuscode = self.request_text.status_code
        self.current_header = self.request_text.headers

        self.html_data = html.unescape(self.request_text.text)
        self.output_url = url
        self.raw_data = self.get_data()

        self.output_username = self.raw_data[0]
        self.output_post_date = self.raw_data[1]
        self.output_caption = self.raw_data[2]

    def get_data(self):
        data_head = self.html_data[:9]

        username = "failed to acquire"
        caption = "failed to acquire"
        post_date = "failed to acquire"

        if data_head == '{"graphql':
            json_data = json.loads(self.html_data)
            body = json_data["graphql"]["shortcode_media"]
            username = body["owner"]["username"]
            post_date = self.detect_date(str(json_data))
            caption = body["edge_media_to_caption"]["edges"][0]["node"]["text"].strip()

        return username, post_date, caption

    def detect_date(self, text):
        date_posted = ""
        split_text = text.split()

        for i in range(len(split_text)):
            try:
                if (split_text[i] == "on") and (split_text[i + 1] in self.months):
                    month = split_text[i + 1]
                    day = split_text[i + 2][:-1]
                    year = split_text[i + 3]
                    date_posted = f"{day} {month} {year}"
            except IndexError or KeyError:
                continue
        return date_posted

    def __repr__(self):
        return self.html_data


class EventLog:
    def __init__(self):
        self.url = []
        self.username = []
        self.post_date = []
        self.caption = []
        self.outputfilename = "rcts_output.xlsx"

    def add_event(self, new_url, new_username, new_postdate, new_caption):
        self.url.append(new_url)
        self.username.append(new_username)
        self.post_date.append(new_postdate)
        self.caption.append(new_caption)

    def to_excel(self):
        self.outputfilename = str(input("Output file name: "))
        dict_out = {"url": self.url,
                    "username": self.username,
                    "post_date": self.post_date,
                    "caption": self.caption}
        df = pd.DataFrame(dict_out)
        df.to_excel(self.outputfilename)


if __name__ == '__main__':
    print("DIVISI EKSTERNAL BEM CIT 2021/2022")
    print("REAL TIME COMPETITION TRACKING SYSTEM")
    print("******************\nALWAYS INCLUDE .xlsx FILE FORMAT")
    filename = str(input("Filename/Directory: "))
    main_file = URLFile(filename)
    main_log = EventLog()
    count = 1
    for event_url in main_file.url_list:
        current_event = InstagramData(event_url)
        print(f"{count}. {current_event.output_username}")
        main_log.add_event(new_url=current_event.output_url,
                           new_username=current_event.output_username,
                           new_postdate=current_event.output_post_date,
                           new_caption=current_event.output_caption)
        count += 1
    main_log.to_excel()
