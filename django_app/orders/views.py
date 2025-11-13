from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pika
import json

def index(request):
    return render(request, 'orders/index.html')

@csrf_exempt
def enviar_pedido_form(request):
    if request.method == "GET":
        return render(request, 'orders/enviar_pedido.html')

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({"error": "invalid json"}, status=400)

        produto = data.get("produto")
        valor = data.get("valor")
        quantidade = data.get("quantidade")

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='orders')

        pedido = json.dumps({
            "produto": produto,
            "valor": valor,
            "quantidade": quantidade
        })

        channel.basic_publish(exchange='', routing_key='orders', body=pedido)
        connection.close()

        return JsonResponse({"status": "success"})
