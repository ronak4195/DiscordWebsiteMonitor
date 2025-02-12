# **Website Monitoring System** 🚀  

This project is a **website monitoring system** built using **Flask**, **MySQL**, and **Redis**. It periodically checks the status of configured websites and sends alerts via a **Discord webhook** if a site goes down or recovers.

---

## **📁 Project Structure**  

```
website_monitor/
│── app.py              # Main entry point of the Flask app  
│── config.py           # Configuration settings (DB, Redis, Webhook, etc.)  
│── database.py         # MySQL database connection  
│── monitor.py          # Background website monitoring logic  
│── redis_client.py     # Redis connection setup  
│── webhook.py          # Webhook configuration route  
│── routes/             # API endpoints  
│   ├── sites.py        # Endpoints for adding/removing/listing monitored sites  
│   ├── history.py      # (Optional) Endpoint to retrieve status history  
│   ├── webhook.py      # Endpoint to configure webhook URL  
│── requirements.txt    # Python dependencies  
```

---

## **📌 Features**  

✅ Monitor multiple websites periodically  
✅ Detect site downtime and status changes  
✅ Store website monitoring data in **MySQL**  
✅ Cache latest site statuses in **Redis** for fast access  
✅ Send real-time alerts to **Discord Webhook**  
✅ REST API to add/remove monitored websites dynamically  

---

## **⚙️ Setup Instructions**  

### **1️⃣ Clone the repository**  
```bash
git clone https://github.com/yourusername/website-monitor.git  
cd website-monitor  
```

### **2️⃣ Install dependencies**  
Create a virtual environment and install required packages:  
```bash
python -m venv venv  
source venv/bin/activate  # On Windows: venv\Scripts\activate  
pip install -r requirements.txt  
```

### **3️⃣ Set up MySQL Database**  
```sql
CREATE DATABASE website_monitor;
USE website_monitor;

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

CREATE TABLE IF NOT EXISTS webhooks (
    url VARCHAR(255) PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

CREATE TABLE IF NOT EXISTS status_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    site_id INT NOT NULL,
    status VARCHAR(10) NOT NULL,  -- Example: 'up' or 'down'
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (site_id) REFERENCES monitored_sites(id) ON DELETE CASCADE
)
```

### **4️⃣ Set up Redis (Optional for caching)**  
Ensure **Redis** is installed and running:  
```bash
redis-server --daemonize yes  
```

### **5️⃣ Configure Webhook URL**  
Modify `config.py` with your Discord Webhook URL:  
```python
webhook_url = "https://discord.com/api/webhooks/your-webhook-url"
```

Alternatively, update it dynamically via API:  
```bash
curl -X POST http://127.0.0.1:5000/webhook/ -H "Content-Type: application/json" -d '{"url": "your_webhook_url"}'
```

---

## **🚀 Running the Application**  
```bash
python app.py  
```

The Flask app will start, monitoring websites in the background.  

---

## **📡 API Endpoints**  

### **1️⃣ Add a website to monitor**  
```http
POST /sites/
```
**Request Body (JSON)**  
```json
{
  "url": "https://example.com",
  "expected_status_code": 200,
  "check_interval_seconds": 60
}
```

### **2️⃣ List monitored websites**  
```http
GET /sites/
```

### **3️⃣ Remove a monitored website**  
```http
DELETE /sites/<site_id>
```

### **4️⃣ Update Webhook URL**  
```http
POST /webhook/
```
**Request Body (JSON)**  
```json
{
  "url": "https://discord.com/api/webhooks/your-webhook-url"
}
```

---

## **🔧 Future Enhancements**  
- 📊 **Dashboard UI** for real-time monitoring  
- 📉 **Historical tracking** of website uptime  
- 📌 **SMS/Email notifications** for downtime alerts  
- ⚡ **Multi-threaded monitoring** for improved efficiency  

---

## **💡 Contributing**  
Feel free to fork the project, create a feature branch, and submit a pull request. Contributions are always welcome!  

---

## **🛠️ Technologies Used**  
- **Flask** - Web framework  
- **MySQL** - Database  
- **Redis** - Caching  
- **Requests** - HTTP monitoring  
- **Discord Webhook** - Notifications  

---

### **🌟 Like the project? Give it a star! ⭐**  
Let me know if you need any modifications! 🚀
