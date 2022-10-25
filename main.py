import sqlite3
from dotenv import load_dotenv
import time
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
load_dotenv()

con = sqlite3.connect('slack.db')

con.execute("""CREATE TABLE IF NOT EXISTS SLACK (USERID text, PINGED BOOLEAN NOT NULL CHECK (PINGED IN (0, 1)))""")
con.commit()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.event("app_mention")
def event(say, payload):

    print(payload)
    
    userId = payload['event']['user']

    print(userId)

    cursor = con.execute("""SELECT USERID FROM SLACK WHERE USERID = ?""", (userId,))

    if len(cursor) == 0:
        print('User not in database, adding tagged user')
        con.execute(f"""INSERT INTO SLACK (USERID, PINGED) VALUES ('{userId}', 1)""")
        con.commit()
       
    else:
        print('User in database, updating pinged to true')
        con.execute(f"""UPDATE SLACK SET PINGED = PINGED + 1 WHERE USERID = '{userId}'""")
        con.commit()
        




if __name__ == "__main__":
    SocketModeHandler(app, os.environ.get["SLACK_APP_TOKEN"]).start()
