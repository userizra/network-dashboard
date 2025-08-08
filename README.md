# Network Dashboard

A real-time network monitoring and alerting dashboard using Kafka, InfluxDB, Grafana, and Python microservices.

## Features

- **Simulated Network Metrics:** Python producer generates realistic network data (latency, packet loss, throughput) and streams to Kafka.
- **ETL Pipeline:** Python consumer reads from Kafka and writes metrics to InfluxDB.
- **Visualization:** Grafana dashboards visualize live network metrics from InfluxDB.
- **Alerting:** Automated email alerts when metrics exceed defined thresholds.

## Architecture

```
[Producer] --> [Kafka] --> [Consumer/ETL] --> [InfluxDB] --> [Grafana]
                                         |
                                   [Email Alerts]
```

## Tech Stack

- **Python** (Producer, Consumer, Alerting)
- **Kafka** (Message Broker)
- **InfluxDB** (Time Series Database)
- **Grafana** (Visualization)
- **Docker Compose** (Orchestration)

## Getting Started

### Prerequisites

- Docker & Docker Compose
- Python 3.8+
- (Optional) SMTP credentials for email alerts

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/network-dashboard.git
   cd network-dashboard
   ```

2. **Start the stack:**
   ```bash
   docker compose up -d
   ```

3. **Install Python dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Run the producer:**
   ```bash
   python simulator/producer.py
   ```

5. **Run the consumer:**
   ```bash
   python etl/consumer.py
   ```

6. **(Optional) Configure and run email alerts:**
   - Edit `alerts/email_alert.py` with your SMTP and InfluxDB credentials.
   - Run:
     ```bash
     python alerts/email_alert.py
     ```

7. **Access Grafana:**
   - Visit [http://localhost:3000](http://localhost:3000)
   - Default credentials: `admin` / `admin123`

## Configuration

- **Kafka, InfluxDB, and Grafana** settings are in `docker-compose.yml`.
- **Alert thresholds** are in `alerts/email_alert.py`.

## Screenshots

...

## Roadmap / Improvements

- Add authentication and user management for Grafana.
- Add more advanced alerting (Slack, SMS).
- Deploy to cloud (AWS, Azure, GCP).
- Add CI/CD pipeline.

## License

MIT License

---