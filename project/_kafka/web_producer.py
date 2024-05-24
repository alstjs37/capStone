from kafka import KafkaProducer
from kafka.errors import KafkaError
import logging
import json

logging.basicConfig(level=logging.INFO)

class Producer:

    def __init__(self):
        self._init_kafka_producer()

    def _init_kafka_producer(self):
        # K8s의 Kafka Cluster
        self.kafka_host = '192.168.3.101:31090', '192.168.3.102:31091', '192.168.3.103:31092'
        self.kafka_topic = "input-topic"
        self.producer = KafkaProducer(
            bootstrap_servers=self.kafka_host, value_serializer=lambda v: json.dumps(v).encode(),
        )

    def publish_to_kafka(self, message):
        try:
            self.producer.send(self.kafka_topic, message)
            self.producer.flush()
        except KafkaError as ex:
            logging.error(f"[ERROR] Failed to publish message: {message} with exception: {ex}")
        else:
            logging.info(f"[SUCCESS] Published message {message} into topic {self.kafka_topic}")