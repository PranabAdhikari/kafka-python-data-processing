import json
from confluent_kafka import Consumer, KafkaError

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'localhost:29092',  # Kafka broker address
    'group.id': 'my-group',  # Consumer group ID
    'auto.offset.reset': 'earliest'  # Start reading from the beginning of the topic if no offset is stored
}

# Create a Kafka consumer instance
consumer = Consumer(conf)

# Subscribe to the 'user-login' topic
consumer.subscribe(['user-login'])

# Continuously poll for new messages
while True:
    # Poll for messages, with a timeout of 1.0 second
    msg = consumer.poll(1.0)

    # Check if no message is received
    if msg is None:
        continue

    # Check for errors in the message
    if msg.error():
        # Handle partition end-of-file error by continuing to poll
        if msg.error().code() == KafkaError._PARTITION_EOF:
            continue
        else:
            # Print other errors and break the loop
            print(msg.error())
            break

    try:
        # Decode the JSON message
        message_data = json.loads(msg.value().decode('utf-8'))

        # Extract relevant information from the message
        user_id = message_data.get('user_id')
        app_version = message_data.get('app_version')
        device_type = message_data.get('device_type')

        # Example processing: Creating a dictionary with processed data
        processed_data = {
            'user_id': user_id,
            'processed_info': f"App Version: {app_version}, Device Type: {device_type}",
            'timestamp': message_data.get('timestamp')
        }

        # Print the processed data
        print(json.dumps(processed_data, indent=2))

    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"Error decoding JSON: {e}")

# Close the Kafka consumer
consumer.close()
