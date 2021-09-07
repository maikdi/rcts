from __future__ import unicode_literals

import argparse
import json
import sys
from io import open
import db_excel

from inscrawler import InsCrawler
from inscrawler.settings import prepare_override_settings

accounts_txt = open('test1.txt', "r")
accounts_list = accounts_txt.read().split(',')

posts_to_take = 1
new_events = {"url": [], "caption": []}

months = ["January", "February", "March",
          "April", "May", "June",
          "July", "August", "September",
          "October", "Novemeber", "December"]


def usage():
    return """
        python crawler.py posts -u cal_foodie -n 100 -o ./output
        python crawler.py posts_full -u cal_foodie -n 100 -o ./output
        python crawler.py profile -u cal_foodie -o ./output
        python crawler.py profile_script -u cal_foodie -o ./output
        python crawler.py hashtag -t taiwan -o ./output

        The default number for fetching posts via hashtag is 100.
    """


def get_posts_by_user(username, number, debug):
    ins_crawler = InsCrawler(has_screen=debug)
    return ins_crawler.get_user_posts(username, number)


def get_profile(username):
    ins_crawler = InsCrawler()
    return ins_crawler.get_user_profile(username)


def arg_required(args, fields=[]):
    for field in fields:
        if not getattr(args, field):
            parser.print_help()
            sys.exit()


def detect_parameters(text):
    date_posted = ""
    tagged = []
    split_text = text.split()
    for word_index in range(len(split_text)):
        count = word_index
        try:
            if (split_text[word_index] == "on") and (split_text[word_index + 1] in months):
                date_posted = f"{split_text[word_index + 1]} {split_text[word_index + 2]} {split_text[word_index + 3]}"
            elif split_text[word_index] == "tagging":
                while split_text[count] != "May":
                    tagged_acc = split_text[count + 1]
                    if tagged_acc[-1] == ".":
                        tagged_acc = tagged_acc[1:-1]
                    if tagged_acc != "May":
                        tagged.append(tagged_acc)
                    count += 1
        except:
            continue
    return date_posted, tagged


def output(account_username, data):
    out = json.dumps(data, ensure_ascii=False)
    meng_dict = json.loads(out[1:-1])
    post_url = meng_dict["key"]
    post_caption = meng_dict["caption"]
    params = detect_parameters(post_caption)
    date_posted = params[0]
    tagged_accounts = str(params[1])
    return account_username, post_url, post_caption, date_posted, tagged_accounts


if __name__ == "__main__":

    db = db_excel.DatabaseConnection()

    parser = argparse.ArgumentParser(description="Instagram Crawler", usage=usage())
    parser.add_argument("mode", help="options: [posts, posts_full, profile, profile_script, hashtag]")
    parser.add_argument("-n", "--number", type=int, help="number of returned posts")
    parser.add_argument("-u", "--username", help="instagram's username")
    parser.add_argument("-t", "--tag", help="instagram's tag name")
    parser.add_argument("-o", "--output", help="output file name(json format)")
    parser.add_argument("--debug", action="store_true")

    prepare_override_settings(parser)

    args = parser.parse_args()

    args.username = "calvinuni"
    args.number = posts_to_take
    args.mode = "posts"
    args.debug = False
    args.output = "./output"
    log_output = db_excel.Event("testing.xlsx")
    for i in range(len(accounts_list)):
        try:
            args.username = accounts_list[i]
            current_output = output(args.username,
                                    get_posts_by_user(args.username,
                                                      args.number,
                                                      args.mode == "posts_full"))
            out_username, out_url, out_caption, out_postdate, out_tagged = current_output
            log_output.add_data(username=out_username,
                                url=out_url,
                                caption=out_caption,
                                dateposted=out_postdate,
                                taggedaccounts=out_tagged)
            db.log(database="rcts_log",
                   table="testing",
                   username=out_username,
                   url=out_url,
                   caption=out_caption,
                   postdate=out_postdate,
                   tagged_account=out_tagged)

            print(f"Successfully acquired from {args.username}")
        except:
            print(f"Failed to acquire from {args.username}.")
            continue
    log_output.create_excel()