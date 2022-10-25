import sqlite3
import time
import re
from slack_bolt import App
import json
from slack_bolt.adapter.socket_mode import SocketModeHandler

with open("settings.json", "r") as f:
    settings = json.load(f)

#Create database if it doesn't exist
con = sqlite3.connect('slack.db')
con.execute("""CREATE TABLE IF NOT EXISTS SLACK (USERID text, PINGED BOOLEAN NOT NULL CHECK (PINGED IN (0, 1)))""")
con.commit()
con.close()

app = App(token=settings["SLACK_BOT_TOKEN"], signing_secret= settings['SLACK_SIGNING_SECRET'])

@app.event("message")
def event(say, payload):


    userId = payload['user']

    text = payload['text']
    
    #Check if the message contains a ping
    if re.search(r'\<\@.*\>', text):
        print('Tagged user found')

    else:
        print('No users were tagged')
        return

    tagged_users = payload['blocks'][0]['elements'][0]['elements']
    
    users = []

    for element in tagged_users:
        if element['type'] == "user":
            users.append(element['user_id'])

    
    for user in users:
        if user == userId:
            continue 
        
        con = sqlite3.connect('slack.db')
        cur = con.cursor()

        databaseUsers = cur.execute("SELECT USERID FROM SLACK WHERE USERID = ?", (user,)).fetchall()

        if len(databaseUsers) == 0:
            cur.execute(f"""INSERT INTO SLACK VALUES (?, 1)""", (user,))
            con.commit()
            con.close()

        else:
            cur.execute(f"""UPDATE SLACK SET PINGED = 1 WHERE USERID = ?""", (user,))
            con.commit()
            con.close()
        
        

   
    


if __name__ == "__main__":
    SocketModeHandler(app, settings["SLACK_APP_TOKEN"]).start()
