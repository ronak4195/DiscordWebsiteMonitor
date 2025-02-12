from flask import Blueprint, request, jsonify
from database import get_db_connection
from monitor import monitor_site, threads, lock
import threading

sites_bp = Blueprint('sites', __name__)

@sites_bp.route('/sites', methods=['POST'])
def add_site():
    data = request.json
    url = data['url']
    expected_status_code = data.get('expected_status_code', 200)
    check_interval = data.get('check_interval_seconds', 60)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("INSERT INTO monitored_sites (url, expected_status_code, check_interval_seconds) VALUES (%s, %s, %s)",
                       (url, expected_status_code, check_interval))
        conn.commit()
        site_id = cursor.lastrowid
    finally:
        cursor.close()
        conn.close()

    thread = threading.Thread(target=monitor_site, args=(site_id, url, expected_status_code, check_interval), daemon=True)

    with lock:
        if thread not in threads:
            thread.start()
            threads.append(thread)

    return jsonify({"message": "Site added", "id": site_id}), 201

@sites_bp.route('/sites/<int:site_id>', methods=['DELETE'])
def remove_site(site_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM monitored_sites WHERE id = %s", (site_id,))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    return jsonify({"message": "Site removed"})

@sites_bp.route('/sites', methods=['GET'])
def list_sites():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM monitored_sites")
        sites = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return jsonify(sites)