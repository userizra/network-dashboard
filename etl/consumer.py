import json
from confluent_kafka import Consumer, KafkaException
from influxdb_client import InfluxDBClient, Point, WritePrecision

KAFKA_BROKER = "kafka:9092"
TOPIC = "network-metrics"
GROUP_ID = "network-metrics-consumer-group"

INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_TOKEN = "my-secret-token"
INFLUXDB_ORG = "network-org"
INFLUXDB_BUCKET = "network-metrics"


def main():
    consumer_conf = {
        'bootstrap.servers': KAFKA_BROKER,
        'group.id': GROUP_ID,
        'auto.offset.reset':'earliest'
    }
    consumer = Consumer(consumer_conf)
    consumer.subscribe([TOPIC])

    influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
    write_api = influx_client.write_api()
    print("Starting Kafka consumer and writing to InfluxDB")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Error: {msg.error()}")
                continue
            
            data = json.loads(msg.value().decode('utf-8'))

            point = Point("network_metrics") \
                .field("latency_ms", data.get("latency_ms")) \
                .field("packet_loss_pct", data.get("packet_loss_pct")) \
                .field("throughput_mbps", data.get("throughput_mbps")) \
                .time(msg.timestamp()[1], WritePrecision.NS)
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            print(f"Written data point to InfluxDB: {data}")
    except KeyboardInterrupt:
        print("Stopping consumer...")
    
    finally:
        consumer.close()
        influx_client.close()

if __name__ == "__main__":
    main()