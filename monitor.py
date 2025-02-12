import threading
import time
import requests
from datetime import datetime, timezone
from database import get_db_connection
from redis_client import redis_client
from webhook import send_discord_alert

threads = []
lock = threading.Lock()

def monitor_sites():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM monitored_sites")
        sites = cursor.fetchall()

        for site in sites:
            site_id = site["id"]
            url = site["url"]
            expected_status_code = site["expected_status_code"]
            check_interval = site["check_interval_seconds"]

            thread = threading.Thread(
                target=monitor_site,
                args=(site_id, url, expected_status_code, check_interval),
                daemon=True
            )
            thread.start()
            threads.append(thread)

    finally:
        cursor.close()
        conn.close()

def monitor_site(site_id, url, expected_status_code, check_interval):
    while True:
        try:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            redis_client.set(f"site_{site_id}_last_change", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
            response_time_ms = int((time.time() - start_time) * 1000)
            current_status = "up" if response.status_code == expected_status_code else "down"
        except requests.RequestException:
            current_status = "down"
            response_time_ms = -1

        previous_status = redis_client.get(f"site_{site_id}")
        previous_status = previous_status.decode('utf-8') if previous_status else "unknown"

        if current_status != previous_status:
            send_discord_alert(url, current_status)
            redis_client.set(f"site_{site_id}", current_status)
            redis_client.set(f"site_{site_id}_last_change", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
            update_site_status_in_db(site_id, current_status)
            print({"url": url, "current_status": current_status})

        print({"url": url, "current_status": current_status, "previous_status": previous_status, "response_time_ms": response_time_ms, "last_checked": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")})

        time.sleep(check_interval)

def update_site_status_in_db(site_id, current_status):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE monitored_sites SET status = %s WHERE id = %s", (current_status, site_id))
        cursor.execute("INSERT INTO status_history (site_id, status) VALUES (%s, %s)", (site_id, current_status))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
