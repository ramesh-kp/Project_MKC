# from azure.eventhub import TransportType
from azure.eventhub import EventHubConsumerClient
Iot_Connection_String = "Endpoint=sb://iothub-ns-mkc-iot-hu-17383143-0e321ed71e.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=CoamC5VpewflsRafv4XBI9nEkxCBJ1FJZXnBC4GUwvA=;EntityPath=mkc-iot-hub"


def on_event_batch(partition_context, events):
    print("jijijijijij")
    for event in events:
        print("Telemetry received::::::::::::: ", event.body_as_str())
        print("Received event from partition::::::::::: {}.".format(
            partition_context.partition_id))
        print("Telemetry received:::::::::::::: ", event.body_as_str())
        print("Properties (set by device)::::::::::::: ", event.properties)
        print("System properties (set by IoT Hub)::::::::::::: ",
              event.system_properties)
        print()
    partition_context.update_checkpoint()


def on_error(partition_context, error):
    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id, error))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


def main():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=Iot_Connection_String, consumer_group="$default",)

    try:
        with client:
            # print("/////////////////////////////////",
            #       client.get_eventhub_properties())
            client.receive_batch(
                on_event_batch=on_event_batch, on_error=on_error)
    except KeyboardInterrupt:
        print("Receiving has stopped.")


if __name__ == '__main__':
    main()
