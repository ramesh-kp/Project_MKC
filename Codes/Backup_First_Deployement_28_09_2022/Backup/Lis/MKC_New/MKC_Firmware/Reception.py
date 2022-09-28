from azure.eventhub import EventHubConsumerClient
from General_Configurations import Receiving_Iot_Connection_String
import json
import threading

file_data = {}
key = 1


def result():
    global file_data
    return file_data


def on_event_batch(partition_context, events):
    global file_data
    global key
    for event in events:
        print("Telemetry received: ", event.body_as_str())
        file_data[key] = event.body_as_str()

    with open('Read_data.json', 'w') as f:
        json.dump(file_data, f)
        key = key + 1

    partition_context.update_checkpoint()
    result()


def on_error(partition_context, error):
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id, error))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


def main():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=Receiving_Iot_Connection_String, consumer_group="$default",)
    try:
        with client:
            client.receive_batch(
                on_event_batch=on_event_batch, on_error=on_error)

    except KeyboardInterrupt:
        print("Receiving has stopped.")
