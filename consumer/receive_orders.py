import pika
import json
import redis

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='orders')
print("👂 Aguardando pedidos na fila 'orders'...")

r = redis.Redis(host='127.0.0.1', port=6379)

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f"✅ Pedido recebido: {order}")

    r.publish('orders_channel', json.dumps(order))

channel.basic_consume(queue='orders', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
