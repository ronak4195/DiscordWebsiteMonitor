from flask import Flask
from routes.sites import sites_bp
from routes.history import history_bp
from monitor import monitor_sites
import threading 
from routes.webhook import webhook_bp
from database import create_tables

app = Flask(__name__)

app.register_blueprint(sites_bp)
app.register_blueprint(history_bp)
app.register_blueprint(webhook_bp)

monitoring_thread = threading.Thread(target=monitor_sites, daemon=True)
monitoring_thread.start()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
