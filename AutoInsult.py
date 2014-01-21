# Auto Insult
# A reddit bot for automatticly insulting people

# Copyright Zach Johnson 2013

'''
 This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


    Please also refer to the stipulations defined in the README file.
'''
# Imports
import praw
import threading
import time

# Arrays
commented = []
blacklist = []
insults3 = ['^^fucktard', '^^moron', '^^idiot', '^^complete ^^faggot']

# Login to Reddit
r = praw.Reddit('Insult Bot by u/_Heckraiser2_ v 1.2.')
print("Logging in...")
r.login("username", "password")
print("Login success.")
print("Importing Ids...")
with open('ids.txt', 'r') as f:
    already_done = [line.strip() for line in f]
print("Ids imported.")

def parse_comment(comment):
    from random import choice
    if (comment not in commented and str(comment.subreddit.display_name) not in blacklist and comment.id not in already_done):
        comment1 = comment.body.lower()
        if ":" in comment1:
                        param, value = comment1.split(":", 1)
                        if value.lower().replace(" ", "") == "autoinsult" or value.lower().replace(" ", "") == "/u/autoinsult" or value.lower().replace(" ", "") == "u/autoinsult" or "autoinsult" in value.lower().replace(" ", "") :
                            print("Self insult attempt found")
                            import random
                            line = random.choice(open('selfinsults.txt').readlines())
                            print(value + " " + line)
                            f = open('commentcount.txt', 'r')
                            counts = f.readline()
                            f.close()
                            counts1 = int(counts)
                            counts3 = str(counts1)
                            comment.reply(line + "\n***\n ^^This ^^insult ^^was ^^generated ^^by ^^a ^^bot ^^you " + choice(insults3) + "." + " ^^I ^^have ^^insulted " + "^^" + counts3 + " ^^people ^^to ^^date. ^^To ^^learn ^^more: [^^AutoInsult](http://pc-tips.net/autoinsult-the-meanest-bot-on-reddit/)")
                            already_done.append(comment.id)
                            with open("ids.txt", "a") as text_file:
                                text_file.write(comment.id + "\n")
                                text_file.close()
                            counts1 += 1
                            f2 = open('commentcount.txt', 'w')
                            f2.write(str(counts1))
                            f2.close()
                        else:
                            print("Comment found insulting")
                            import random
                            line = random.choice(open('insults.txt').readlines())
                            print(value + " " + line)
                            f = open('commentcount.txt', 'r')
                            counts = f.readline()
                            f.close()
                            counts1 = int(counts)
                            counts3 = str(counts1)
                            comment.reply(value.upper() + ", " + line + "\n***\n ^^This ^^insult ^^was ^^generated ^^by ^^a ^^bot ^^you " + choice(insults3) + "." + " ^^I ^^have ^^insulted " + "^^" + counts3 + " ^^people ^^to ^^date. ^^To ^^learn ^^more: [^^AutoInsult](http://pc-tips.net/autoinsult-the-meanest-bot-on-reddit/)")
                            already_done.append(comment.id)
                            with open("ids.txt", "a") as text_file:
                                text_file.write(comment.id + "\n")
                                text_file.close()
                            counts1 += 1
                            f2 = open('commentcount.txt', 'w')
                            f2.write(str(counts1))
                            f2.close()
                   
                   
# Main loop for comment searching and parsing
def main_loop():
    # Main loop start here...
    print("Starting...")
    while True:
        # Read the blacklist and place it into an array
        with open("blacklist.txt", 'r') as f:
            del blacklist[:]
            for entry in f.readlines():
                blacklist.append(entry.strip())

        # Read read list for mentioned
        with open("readlist.txt", 'r') as f:
            readlist = []
            for entry in f.readlines():
                readlist.append(entry.strip())

        # Start the comment loop
        try:
            # Grab as many comments as we can and loop through them
            for comment in r.get_comments("all", limit=None):
                # Check if the comment meets the basic criteria
                if "auto insult:" in comment.body.lower():
                    print("Comment found. Parsing...")
                    parse_comment(comment)

            # Check mentions
            for comment in r.get_mentions():
                print("Checking mentions...")
                if comment.id not in readlist:
                    with open("readlist.txt", "a") as f:
                        f.write(comment.id + '\n')
                    parse_comment(comment)

            # Finally wait 30 seconds
            print("Sleeping...")
            time.sleep(30)
            print("Starting..")
        except Exception as e:
            print(e)

# Threads!
main_thread = threading.Thread(target=main_loop)

# Start threads!
main_thread.start()
