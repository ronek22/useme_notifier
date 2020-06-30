import requests
from crawler import Crawler
import psycopg2
import os
import schedule

api = 'https://api.telegram.org/'
bot_token = os.environ['USEME_TOKEN']
bot_chatID = os.environ['USEME_CHAT_ID'] 

def send_message(chat_id, text):
    parameters = {'chat_id': chat_id, 'text':text, 'parse_mode':'markdown'}
    message = requests.post(f"{api}bot{bot_token}/sendMessage", data=parameters)

def check_result_send_mess():
    print("Checking new jobs...")

    try:
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        jobs_db = conn.cursor()
        jobs_db.execute('CREATE TABLE IF NOT EXISTS jobs (id SERIAL, link TEXT NOT NULL)')
    except Exception as e:
        return send_message(bot_chatID, f'The database could not be accessed\nError code: {e}')

    # crawl jobs from website
    jobs = Crawler().jobs

    for job in jobs:
        job_exists = jobs_db.execute(f"SELECT link FROM jobs WHERE link='{job.link}'")
        if len(jobs_db.fetchall()) != 1:
            mess_content = job.print()
            send_message(bot_chatID, mess_content)
            jobs_db.execute(f"INSERT INTO jobs (link) VALUES ('{job.link}')")
            conn.commit()
        else:
            continue
    
    jobs_db.close()

schedule.every().minute.do(check_result_send_mess)

# infinite loop
while True:
    schedule.run_pending()
