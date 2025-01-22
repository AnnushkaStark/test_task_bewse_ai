import json
import logging

from aiokafka import AIOKafkaProducer

from constants.kafka import KAFKA_TOPIC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_application(application_data: dict) -> None:
    topic = KAFKA_TOPIC
    async with AIOKafkaProducer(
        bootstrap_servers="localhost:9092", retry_backoff_ms=5
    ) as producer:
        try:
            logger.info(f"Sending message to topic: {topic}")
            await producer.start()
            await producer.send_and_wait(
                topic=topic, value=json.dumps(application_data).encode()
            )
            logger.info(f"Message sent successfully to topic: {topic}")
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise
        finally:
            logger.info("Stopping Kafka producer")
            await producer.stop()
