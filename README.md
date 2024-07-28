# Order and Inventory Microservices

# Overview
This project contains two microservices: OrderService and InventoryService, which communicate through Apache Kafka. OrderService allows placing orders, and InventoryService processes those orders by reducing the inventory.


# Prerequisites
- Git
- Python
- Docker
- Docker Compose

# Steps

1. Clone the repository:
    git clone https://github.com/DeepanshuMathur1/microservice-communication-kafka.git
    cd microservice-communication-kafka

2. Build and run the services: To start the application on your local host run the bellow command.
    docker-compose up --build

3. Access the services:
    - OrderService: `http://localhost:5002/order` (POST)  - Will be used to place the orders 
    - InventoryService: `http://localhost:5001/inventory` (GET) - Inventory will be updated and from this GET request we can verify the changes

# Testing

1. Access the services to place orders and check inventory:
    Either dirctly run the below curl on terminal or import it in postman and make a request
    - Place an order:
        
        curl -X POST http://localhost:5002/order -H "Content-Type: application/json" -d '{"item_id": "item1", "quantity": 1}'

    - Get inventory:

        curl http://localhost:5001/inventory


2. Run unit tests:
    - OrderService tests:
        docker-compose run order_service python -m unittest discover -s .

    - InventoryService tests:
        docker-compose run inventory_service python -m unittest discover -s .


# Assumptions and Decisions
This is a python flask based application with an in-memory dictionary for storing the items, we have not used any external database for storing the inventory.