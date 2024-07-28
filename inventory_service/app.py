from flask import Flask, jsonify
from kafka import KafkaConsumer
import json
import threading
import logging
import time

app = Flask(__name__)
inventory = {'item1': 100, 'item2': 200}
logging.basicConfig(level=logging.INFO)

def get_kafka_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                'orders',
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                group_id='inventory-service',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logging.info("Kafka consumer connected successfully.")
            return consumer
        except Exception as e:
            logging.error(f"Kafka broker not available, retrying {str(e)}")
            time.sleep(5)

def consume_orders():
    consumer = get_kafka_consumer()
    for message in consumer:
        order = message.value
        logging.info(f"Received order: {order}")
        item_id = order['item_id']
        quantity = order['quantity']
        if item_id in inventory:
            if inventory[item_id] >= quantity:
                inventory[item_id] -= quantity
                logging.info(f"Processed order: {order}. Updated inventory: {inventory}")
            else:
                logging.warning(f"Not enough inventory for item {item_id}. Order: {order}")
        else:
            logging.warning(f"Item {item_id} does not exist. Order: {order}")

@app.route('/inventory', methods=['GET'])
def get_inventory():
    return jsonify(inventory)

if __name__ == '__main__':
    # Ensure the Kafka consumer runs in a separate thread
    consumer_thread = threading.Thread(target=consume_orders, daemon=True)
    consumer_thread.start()
    app.run(host='0.0.0.0', port=5001)
