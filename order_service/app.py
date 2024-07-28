from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import requests
import time

app = Flask(__name__)

# Retry mechanism for Kafka connection
def get_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            return producer
        except Exception as e:
            print(f"Kafka broker not available, retrying... {str(e)}")
            time.sleep(5)

producer = get_kafka_producer()

INVENTORY_SERVICE_URL = 'http://inventory_service:5001/inventory'

@app.route('/order', methods=['POST'])
def place_order():
    order_data = request.get_json()
    if 'item_id' not in order_data or 'quantity' not in order_data:
        return jsonify({'error': 'Invalid order format'}), 400
    
    item_id = order_data['item_id']
    quantity = order_data['quantity']
    
    response = requests.get(INVENTORY_SERVICE_URL)
    inventory = response.json()
    
    if item_id not in inventory or inventory[item_id] < quantity:
        return jsonify({'error': f'Not enough inventory for item {item_id}'}), 400
    
    try:
        producer.send('orders', order_data)
        producer.flush()
        return jsonify({'message': 'Order placed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)