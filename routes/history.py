from flask import Blueprint, jsonify
from database import get_db_connection

history_bp = Blueprint('history', __name__)

@history_bp.route('/sites/<int:site_id>/history', methods=['GET'])
def get_status_history(site_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM status_history WHERE site_id = %s ORDER BY checked_at DESC", (site_id,))
        history = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return jsonify(history) if history else jsonify({"error": "No history found"}), 404
