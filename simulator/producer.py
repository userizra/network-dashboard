import json
import random
import time
from confluent_kafka import Producer


# Kafka broker address - use service name and port from your docker-compose
KAFKA_BROKER = "kafka:9092"
TOPIC = "network-metrics"

producer = Producer({'bootstrap.servers':KAFKA_BROKER})

def generate_metrics():
    """
    # Generate a fake network metric dict:
    - latency in ms
    - packet_loss in percentage
    - throughput in Mbps
    """
    metrics = {
        "latency_ms": round(random.uniform(10, 150), 2),            # 10-150ms
        "packet-loss_pct": round(random.uniform(0, 5), 2),          # 0-5%
        "throughput_mbps": round(random.uniform(50,1000), 2)        # 50-1000 Mbps
    }
    return metrics

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")


def main():
    print(f"Starting simulator, producing to topic '{TOPIC}' at broker {KAFKA_BROKER}")
    try:
        while True:
            metrics = generate_metrics()
            message = json.dumps(metrics)
            producer.produce(TOPIC, message.encode('utf-8'), callback = delivery_report)
            producer.poll(0)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping producer...")
    finally:
        producer.flush(2)  # Add a timeout here
        
if __name__ == "__main__":
    main()