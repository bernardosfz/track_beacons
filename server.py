import pika
from config import RABBIT_CONFIG

def callback(ch, method, properties, body):
    message = body.decode('utf-8')
    #message = {
	#'antena': 1, 
	#'datahora': '2025-06-11T19:41:46.304379', 
	#'beacon': '2F234454-CF6D-4A0F-ADF2-F4911BA9FFA6', 
	#'rssi': -37, 
	#'mac': '40:22:2E:44:B1:CC'
#}
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Mensagem recebida: {message}")

try:
    params = pika.URLParameters(RABBIT_CONFIG)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    channel.exchange_declare(exchange='track_beacons', exchange_type='topic', durable=True)
    channel.queue_declare(queue='tracking')
    channel.queue_bind(exchange='track_beacons', queue='tracking', routing_key='tracking')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='tracking', on_message_callback=callback)

    print("Consumidor está aguardando mensagens...")

    while True:
        channel.connection.process_data_events(time_limit=10)
except KeyboardInterrupt:
    print("Saiu")