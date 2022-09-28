# import json
# from azure.eventhub import EventHubConsumerClient
# from Configurations import Receiving_Iot_Connection_String

# file_data = {}
# key = 1


# class ReadFromIoT:
#     # @staticmethod
#     def result(self):
#         global file_data
#         return file_data

#     def on_event_batch(self, partition_context, events):
#         global file_data
#         global key
#         for event in events:
#             print("Telemetry_received", event.body_as_str())
#             file_data[key] = event.body_as_str()

#         with open("Read_Check.json", 'w') as f:
#             json.dump(file_data, f)
#             key = key + 1

#         partition_context.update_checkpoint()
#         self.result()

#     # @staticmethod
#     def on_error(self, partition_context, error):
#         if partition_context:
#             print("An exception: {} occurred during receiving from Partition: {}.".format(
#                 partition_context.partition_id, error))
#         else:
#             print(
#                 "An exception: {} occurred during the load balance process.".format(error))

#     def eventhub_connect(self):
#         try:
#             client = EventHubConsumerClient.from_connection_string(
#                 conn_str=Receiving_Iot_Connection_String, consumer_group="$default",)
#             with client:
#                 client.receive_batch(
#                     on_event_batch=self.on_event_batch, on_error=self.on_error)

#         except KeyboardInterrupt:
#             print("Receiving_has_stopped")

# ReadFromIoT().eventhub_connect()
# *******************************************
import os
import sys
import logging
import time
from azure.eventhub import EventHubClient, Receiver, Offset


logger = logging.getLogger("azure")

ADDRESS = ""
USER = ""
KEY = ""

CONSUMER_GROUP = "$default"
OFFSET = Offset("@latest")
PARTITION = "2"

total = 0
last_sn = -1
last_offset = "-1"
client = EventHubClient(ADDRESS, debug=False, username=USER, password=KEY)

receiver = client.add_receiver(
    CONSUMER_GROUP, PARTITION, prefetch=0, offset=OFFSET)
client.run()
start_time = time.time()
while True:
    for event_data in receiver.receive(timeout=5000):
        print("Received: {}".format(event_data.body_as_str(encoding='UTF-8')))
        a = event_data.body_as_str(encoding='UTF-8')
        total += 1
    end_time = time.time()
    run_time = end_time - start_time
    print("Received {} messages in {} seconds".format(total, run_time))
