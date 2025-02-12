import requests
from database import get_db_connection

def send_discord_alert(site_url, status):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT url FROM webhooks")
        urls = cursor.fetchall()

        if not urls:
            print("No webhook URL found in the database!")
            return

        webhook_url = urls[0]['url'] 

        if webhook_url is None:
            print("Webhook URL is not set!")
            return

        message = {
            "content": f"{':rotating_light:' if status == 'down' else ':white_check_mark:'} The site {site_url} is {status}!"
        }
        try:
            requests.post(webhook_url, json=message)
        except requests.RequestException as e:
            print(f"Failed to send Discord alert: {e}")
    finally:
        cursor.close()
        conn.close()
