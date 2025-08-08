import smtplib
from email.mime.text import MIMEText
from influxdb_client import InfluxDBClient
import time

# InfluxDB configs
INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_TOKEN = "my-secret-token"
INFLUXDB_ORG = "network-org"
INFLUXDB_BUCKET = "network-metrics"

# Email configs
SMTP_SERVER = "smtp.gmail.com"  # or your SMTP server
SMTP_PORT = 587
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASS = "your_email_password"
EMAIL_TO = "alert_recipient@example.com"

# Thresholds for alerts
THRESHOLDS = {
    "latency_ms": 100,
    "packet_loss_pct": 1,
    "throughput_mbps": 100,  # e.g., alert if throughput below 100 Mbps
}

def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Secure the connection
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        print("Alert email sent!")

def query_latest_metrics(client):
    query = f'''
    from(bucket:"{INFLUXDB_BUCKET}")
      |> range(start: -5m)
      |> last()
    '''
    tables = client.query_api().query(query, org=INFLUXDB_ORG)
    result = {}
    for table in tables:
        for record in table.records:
            result[record.get_field()] = record.get_value()
    return result

def check_thresholds(metrics):
    alerts = []
    if metrics.get("latency_ms", 0) > THRESHOLDS["latency_ms"]:
        alerts.append(f"Latency high: {metrics['latency_ms']} ms")

    if metrics.get("packet_loss_pct", 0) > THRESHOLDS["packet_loss_pct"]:
        alerts.append(f"Packet loss high: {metrics['packet_loss_pct']} %")

    if metrics.get("throughput_mbps", float('inf')) < THRESHOLDS["throughput_mbps"]:
        alerts.append(f"Throughput low: {metrics['throughput_mbps']} Mbps")

    return alerts

def main():
    influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

    while True:
        metrics = query_latest_metrics(influx_client)
        if metrics:
            print(f"Latest metrics: {metrics}")
            alerts = check_thresholds(metrics)
            if alerts:
                subject = "Network Metrics Alert"
                body = "\n".join(alerts)
                send_email(subject, body)
            else:
                print("All metrics within threshold.")
        else:
            print("No metrics found.")

        time.sleep(300)  # Wait 5 minutes before checking again

if __name__ == "__main__":
    main()
