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
con.execute("""CREATE TABLE IF NOT EXISTS SLACK (LINK text, USERPINGER text, USERPINGED text, PINGED BOOLEAN NOT NULL CHECK (PINGED IN (0, 1)))""")
con.commit()
con.close()

app = App(token=settings["SLACK_BOT_TOKEN"], signing_secret= settings['SLACK_SIGNING_SECRET'])


@app.event("app_home_opened")
def update_home_tab(client, event, logger):

    # Get the user ID associated with the event
    user_id = event["user"]

    # Check if user is in the database and fetch all 

    con = sqlite3.connect('slack.db')
    cur = con.cursor()
    users = cur.execute("SELECT USERPINGED FROM SLACK WHERE USERPINGED = ?", (user_id,))
    users = users.fetchall()

    print(users)
    con.close()

    # If user is in the database, fetch all links and USERPINGER send them to the user
    if users:
        con = sqlite3.connect('slack.db')
        cur = con.cursor()
        links = cur.execute("SELECT LINK, USERPINGER FROM SLACK WHERE USERPINGED = ?", (user_id,))
        links = links.fetchall()
        con.close()

        # Create a list of blocks
        blocks = []

        for link in links:
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Someone pinged you in a thread: {link[0]}",
                    },
                }
            )
            blocks.append(
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"User who pinged you: <@{link[1]}>",
                    },
                }
            )
            blocks.append(
                {
                    "type": "divider",
                }
            )

        app.client.views_publish(user_id= user_id, view= {
        "type":"home",
        "blocks": blocks
        })

        # Send the message back to Slack
    else:
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "You have no pings",
                },
            }
        ]

        app.client.views_publish(user_id= user_id, view= {
        "type":"home",
        "blocks": blocks
        })
        

    




@app.event("message")
def event(say, payload):


    userId = payload['user']


    message_link = app.client.chat_getPermalink(channel=payload['channel'], message_ts=payload['ts'])['permalink']

    print(message_link)
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
        #if user == userId:
            #continue 
        
        con = sqlite3.connect('slack.db')
        cur = con.cursor()
        
        cur.execute(f"""INSERT INTO SLACK VALUES (?, ?, ?, 1)""", (message_link, userId, user,))
        con.commit()
        con.close()

        

   
    


if __name__ == "__main__":
    SocketModeHandler(app, settings["SLACK_APP_TOKEN"]).start()
