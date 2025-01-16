from aiokafka import AIOKafkaProducer

from constants.kafka import KAFKA_TOPIC

topic = KAFKA_TOPIC


async def send_application(application_data: dict) -> None:
    producer = AIOKafkaProducer(bootstrap_servers="kafka:9092")
    await producer.start()
    try:
        await producer.send_and_wait(topic=topic, value=application_data)
    except Exception as e:
        raise Exception(str(e))
    finally:
        await producer.stop()
