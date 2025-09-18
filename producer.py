# from kafka import KafkaProducer
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# import json, time
# from kafka.errors import NoBrokersAvailable, KafkaTimeoutError

# # Retry until Kafka is ready
# # while True:
# #     try:
# #         producer = KafkaProducer(
# #             bootstrap_servers='kafka:9092',  # remove 'http://'
# #             value_serializer=lambda v: json.dumps(v).encode('utf-8')
# #         )
# #         break
# #     except NoBrokersAvailable:
# #         print("Waiting for Kafka broker...")
# #         time.sleep(5)


# while True:
#     try:
#         producer = KafkaProducer(
#             bootstrap_servers='localhost:9092',
#             value_serializer=lambda v: json.dumps(v).encode('utf-8')
#         )
#         producer.partitions_for('file_uploads')  # force metadata lookup
#         break
#     except (NoBrokersAvailable, KafkaTimeoutError):
#         print("Waiting for Kafka broker and topic...")
#         time.sleep(5)

# class UploadHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         if not event.is_directory:
#             producer.send('file_uploads', {'filename': event.src_path})
#             print(f"Sent Kafka event: {event.src_path}")

# observer = Observer()
# observer.schedule(UploadHandler(), path="./data/raw", recursive=False)
# observer.start()

# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     observer.stop()
# observer.join()
import json, time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import NoBrokersAvailable, KafkaTimeoutError, TopicAlreadyExistsError

KAFKA_BOOTSTRAP = "localhost:29092"
TOPIC = "file_uploads"

# Ensure topic exists on startup
admin = KafkaAdminClient(bootstrap_servers=KAFKA_BOOTSTRAP)
try:
    admin.create_topics([NewTopic(name=TOPIC, num_partitions=1, replication_factor=1)])
    print(f"Topic '{TOPIC}' created.")
except TopicAlreadyExistsError:
    print(f"Topic '{TOPIC}' already exists.")

# Connect with retries
while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        producer.partitions_for(TOPIC)
        break
    except (NoBrokersAvailable, KafkaTimeoutError):
        print("Waiting for Kafka broker and topic…")
        time.sleep(5)

class UploadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            producer.send(TOPIC, {"filename": event.src_path})
            print(f"Sent Kafka event: {event.src_path}")

observer = Observer()
observer.schedule(UploadHandler(), path="./data/raw", recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()

