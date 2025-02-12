import mysql.connector
from config import db_config

def get_db_connection():
    return mysql.connector.connect(**db_config)

def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_sites (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url VARCHAR(2083) NOT NULL,
            check_interval_seconds INT NOT NULL DEFAULT 300,
            name VARCHAR(255) NOT NULL DEFAULT 'unknown',
            expected_status_code INT NOT NULL DEFAULT 200,
            status ENUM('unknown','up','down') NOT NULL DEFAULT 'unknown',
            response_time_ms INT,
            last_checked DATETIME,
            last_status_change DATETIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS webhooks (
            url VARCHAR(255) PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS status_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            site_id INT NOT NULL,
            status VARCHAR(10) NOT NULL,  -- Example: 'up' or 'down'
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (site_id) REFERENCES monitored_sites(id) ON DELETE CASCADE
        )
    ''')
    
    connection.commit()
    cursor.close()
    connection.close()
