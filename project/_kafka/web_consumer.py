from kafka import KafkaConsumer
import logging

logging.basicConfig(level=logging.INFO)

class Consumer:

    def __init__(self):
        self._init_kafka_consumer()

    def _init_kafka_consumer(self):
        # 외부 -> k8s 
        self.kafka_host = '192.168.3.101:31090', '192.168.3.102:31091', '192.168.3.103:31092'
        self.kafka_topic = "output-topic"
        self.consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=self.kafka_host,
        )

    def consume_from_kafka(self):
        for message in self.consumer:
            logging.info(message.value)
            
            print("\n[MESSAGE] : " + str(message.value) + "\n")
            return message.value.decode('utf-8')