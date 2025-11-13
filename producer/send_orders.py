import pika
import json
import time
import random

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='orders')

print(" Enviando pedidos para RabbitMQ... (Ctrl+C para parar)\n")

try:
    while True:
        order_id = random.randint(1000, 9999)
        order = {
            "id": order_id,
            "product": random.choice(["Camisa", "Boné", "Calça", "Tênis"]),
            "value": round(random.uniform(50, 500), 2)
        }
        message = json.dumps(order)
        channel.basic_publish(exchange='', routing_key='orders', body=message)
        print(f" Pedido enviado: {order}")
        time.sleep(5)
except KeyboardInterrupt:
    print("\n Parando envio de pedidos.")
    connection.close()
