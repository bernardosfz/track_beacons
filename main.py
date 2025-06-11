import asyncio
from bleak import BleakScanner
import datetime
import pika
import json
from config import RABBIT_CONFIG
import serial
import time

antena = 1

#serial_port_name = '/dev/ttyACM0'
#serial_port = serial.Serial(serial_port_name, 9600)
time.sleep(2)

TARGET_UUIDS = [
    "2F234454-CF6D-4A0F-ADF2-F4911BA9FFA6",
    "967D8C06-7E9D-44C3-9E12-43DCC0E6C1F6"
]

#parameters = pika.URLParameters(RABBIT_CONFIG)
#connection = pika.BlockingConnection(parameters)
#channel = connection.channel()

#channel.exchange_declare(exchange='track_beacons', exchange_type='topic', durable=True)
#channel.queue_declare(queue='tracking')

async def main():
    targets = [uuid.lower().replace('-', '') for uuid in TARGET_UUIDS]
    print(f"Tracking Beacons")

    while True:
        beacons = await BleakScanner.discover(timeout=5.0)
        data_hora = datetime.datetime.now().isoformat()

        for b in beacons:
            if 'manufacturer_data' in b.metadata:
                if hasattr(b, 'rssi') and b.rssi > -49:
                    for data in b.metadata['manufacturer_data'].values():
                        hex_data = data.hex()
                        for i, target in enumerate(targets):
                            if target in hex_data:
                                uuid_detectado = TARGET_UUIDS[i]
                                #serial_port.write(b"1\n")
                                message = {
                                    "antena": antena,
                                    "datahora": data_hora,
                                    "beacon": uuid_detectado,
                                    "rssi": b.rssi,
                                    "mac": b.address
                                }
                                print(message)
                                #channel.basic_publish(exchange='track_beacons',routing_key='tracking',body=json.dumps(message),properties=pika.BasicProperties(delivery_mode=2))
                                break
        await asyncio.sleep(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Parado")
