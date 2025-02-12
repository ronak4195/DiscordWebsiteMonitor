---

# **Website Monitoring Service**

This service monitors websites, logs status changes, and sends alerts via **Discord Webhooks**. It uses **Flask**, **MySQL**, and **Redis** for efficient monitoring and alerting.

---

## **Project Structure**
```
website_monitor/
│── app.py                # Main Flask application
│── config.py             # Configuration settings (Database & Redis)
│── database.py           # Database connection and table creation
│── monitor.py            # Website monitoring logic (threads & status checks)
│── redis_client.py       # Redis client connection setup
│── discord.py            # Discord notification management
│── routes/               # Flask Blueprints for routes
│   ├── sites.py          # Routes for managing monitored sites
│   ├── history.py        # Routes for retrieving status history
│   ├── webhook.py        # Routes for configuring webhooks
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
```

---

## **Installation and Setup**
### **1. Clone the repository**
```bash
git clone https://github.com/yourusername/website_monitor.git
cd website_monitor
```

### **2. Install dependencies**
Create a virtual environment and install the required packages:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
pip install -r requirements.txt
```

### **3. Configure Database & Redis**
Ensure **MySQL** and **Redis** are running. Update `config.py` with your database credentials:
```python
db_config = {
    "host": "localhost",
    "user": "username",
    "password": "password",
    "database": "website_monitor"
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
```

### **4. Create Database Tables**
Run the following command to initialize the database:
```bash
python -c "from database import create_tables; create_tables()"
```
Alternatively, run these SQL commands in MySQL manually:

```sql
CREATE DATABASE website_monitor;

USE website_monitor;

CREATE TABLE monitored_sites (
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
);

CREATE TABLE webhooks (
    url VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE status_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    site_id INT NOT NULL,
    status VARCHAR(10) NOT NULL,  
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (site_id) REFERENCES monitored_sites(id) ON DELETE CASCADE
);
```

### **5. Run the Application**
```bash
python app.py
```
The server starts on **http://127.0.0.1:5000**

---

## **Database Tables Overview**
### **1. `monitored_sites`**
Stores details of websites being monitored.
```sql
CREATE TABLE monitored_sites (
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
);
```

| Column Name         | Type            | Description |
|---------------------|----------------|-------------|
| `id`               | INT (Primary Key) | Unique identifier for each website |
| `url`              | VARCHAR(2083)   | Website URL |
| `check_interval_seconds` | INT       | Frequency of checks (default 300 seconds) |
| `name`             | VARCHAR(255)    | Site name (default: "unknown") |
| `expected_status_code` | INT        | Expected HTTP response code (default: 200) |
| `status`           | ENUM('unknown', 'up', 'down') | Current site status |
| `response_time_ms` | INT             | Last recorded response time in milliseconds |
| `last_checked`     | DATETIME        | Last time the site was checked |
| `last_status_change` | DATETIME       | Last time the site status changed |
| `created_at`       | TIMESTAMP       | Time the record was created |

---

### **2. `webhooks`**
Stores Discord Webhook URLs for alerts.
```sql
CREATE TABLE webhooks (
    url VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

| Column Name   | Type        | Description |
|--------------|------------|-------------|
| `url`       | VARCHAR(255) | Webhook URL (Primary Key) |
| `created_at` | TIMESTAMP   | Time of webhook registration |

---

### **3. `status_history`**
Logs all website status changes.
```sql
CREATE TABLE status_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    site_id INT NOT NULL,
    status VARCHAR(10) NOT NULL,  
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (site_id) REFERENCES monitored_sites(id) ON DELETE CASCADE
);
```

| Column Name | Type        | Description |
|------------|------------|-------------|
| `id`       | INT (Primary Key) | Unique log entry ID |
| `site_id`  | INT (Foreign Key) | Reference to `monitored_sites.id` |
| `status`   | VARCHAR(10) | Status of the site (`up` or `down`) |
| `checked_at` | TIMESTAMP   | Time of the status check |

---

## **How Website Monitoring Works**
1. **Fetch monitored sites:**  
   `monitor.py` retrieves the list of monitored websites from the database.
   
2. **Start monitoring threads:**  
   A separate thread is created for each website, which checks its status every `check_interval_seconds`.

3. **Check website status:**  
   - Sends an HTTP GET request to the site.
   - Compares the response status code with `expected_status_code`.
   - Updates **Redis** with the latest status.
   - If the status changes, an entry is added to **status_history** in MySQL.

4. **Send alerts on status change:**  
   If the status changes from **up** to **down** or vice versa, a **Discord alert** is sent.

5. **Store status history:**  
   - Current status is stored in `monitored_sites`.
   - Status changes are logged in `status_history`.

---

## **Key Functions in `database.py`**
### **1. `get_db_connection()`**
Creates and returns a MySQL connection.
```python
def get_db_connection():
    return mysql.connector.connect(**db_config)
```

### **2. `create_tables()`**
Creates the necessary database tables if they do not exist.
```python
def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute("CREATE TABLE IF NOT EXISTS monitored_sites (...);")
    cursor.execute("CREATE TABLE IF NOT EXISTS webhooks (...);")
    cursor.execute("CREATE TABLE IF NOT EXISTS status_history (...);")

    connection.commit()
    cursor.close()
    connection.close()
```
- This function should be run before starting the application.

---

## **Technologies Used**
- **Flask** - Web framework
- **MySQL** - Database
- **Redis** - Caching and quick status retrieval
- **Threading** - Concurrent website monitoring
- **Discord Webhooks** - Notifications

## **Future Enhancements**
- ✅ Add **email notifications**  
- ✅ Implement **frontend dashboard**  
- ✅ Improve **thread management**  

---

This **README** now includes everything about the **database setup**! 🚀 Let me know if you need modifications.
