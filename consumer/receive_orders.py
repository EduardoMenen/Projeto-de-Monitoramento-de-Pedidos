import os
import sys
import json
from pathlib import Path
import pika
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

BASE_DIR = Path(__file__).resolve().parent.parent
DJANGO_APP_PATH = BASE_DIR / "django_app"
sys.path.append(str(DJANGO_APP_PATH))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "order_monitor.settings")

try:
    import django
    django.setup()
except Exception as e:
    print("Erro ao inicializar Django:", e)
    raise

pedido_id = 0

def main():
    global pedido_id

    print("🔊 Aguardando pedidos na fila 'orders'...")

    params = pika.ConnectionParameters(host='localhost', heartbeat=600, blocked_connection_timeout=300)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='orders')

    def callback(ch, method, properties, body):
        global pedido_id

        try:
            data = json.loads(body.decode('utf-8'))
            pedido_id += 1
            print("📦 Pedido recebido!")
            print(f"  ID Pedido: {pedido_id}")
            print(f"  Produto:   {data.get('produto')}")
            print(f"  Valor:     {data.get('valor')}")
            print(f"  Quantidade:{data.get('quantidade')}")
            print("-" * 40)

            try:
                layer = get_channel_layer()
                async_to_sync(layer.group_send)(
                    "orders_group",
                    {
                        "type": "send_new_order",
                        "message": (
                            f"<strong>Pedido {pedido_id}</strong><br>"
                            f"Produto: {data.get('produto')}<br>"
                            f"Valor: R$ {data.get('valor')}<br>"
                            f"Quantidade: {data.get('quantidade')} un"
                        )
                    }
                )
            except Exception as e:
                print("Erro ao enviar para Channels:", e)

        except Exception as e:
            print("Erro ao processar mensagem:", e)

    channel.basic_consume(queue='orders', on_message_callback=callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Interrompido pelo usuário")
    except Exception as e:
        print("Erro no consumer:", e)
    finally:
        if connection and connection.is_open:
            connection.close()

if __name__ == "__main__":
    main()