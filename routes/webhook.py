from flask import Blueprint, request, jsonify
from database import get_db_connection

webhook_bp = Blueprint('webhook', __name__)

@webhook_bp.route('/webhook', methods=['POST'])
def configure_webhook():
    data = request.json
    webhook_url = data.get('url', None) 

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("DELETE FROM webhooks")
        cursor.execute("INSERT INTO webhooks (url) VALUES (%s)", (webhook_url,))
        conn.commit()
        site_id = cursor.lastrowid
        return jsonify({"message": "Webhook URL configured successfully", "id": site_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
