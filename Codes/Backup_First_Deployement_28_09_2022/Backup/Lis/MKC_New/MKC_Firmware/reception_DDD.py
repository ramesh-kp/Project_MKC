# from Azure_Communication import Receive_Azure_Data
# from azure.eventhub import TransportType
# from azure.eventhub import EventHubConsumerClient
# Receiving_Iot_Connection_String = "Endpoint=sb://iothub-ns-mkc-iot-hu-17383143-0e321ed71e.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=CoamC5VpewflsRafv4XBI9nEkxCBJ1FJZXnBC4GUwvA=;EntityPath=mkc-iot-hub"


# def on_event_batch(partition_context, events):
#     for event in events:
#         Receive_Azure_Data().Azure_Read(event.body_as_str())
#     partition_context.update_checkpoint()


# def on_error(partition_context, error):
#     if partition_context:
#         print("An exception: {} occurred during receiving from Partition: {}.".format(
#             partition_context.partition_id, error))
#     else:
#         print("An exception: {} occurred during the load balance process.".format(error))


# def main():
#     client = EventHubConsumerClient.from_connection_string(
#         conn_str=Receiving_Iot_Connection_String, consumer_group="$default",)
#     try:
#         with client:
#             client.receive_batch(
#                 on_event_batch=on_event_batch, on_error=on_error)
#     except KeyboardInterrupt:
#         print("Receiving has stopped.")


# if __name__ == '__main__':
#     main()
