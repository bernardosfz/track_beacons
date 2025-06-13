import pika
import json
import sqlite3
import os
from datetime import datetime
from config import RABBIT_CONFIG

DB_PATH = 'tracking_database.db'

def init_database():
    db_exists = os.path.exists(DB_PATH)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ANTENA (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        local TEXT
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS BEACON (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        uuid TEXT UNIQUE,
        mac TEXT
    )''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TRACKING (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        datahora TEXT,
        beacon_id INTEGER,
        antena_id INTEGER,
        rssi INTEGER,
        FOREIGN KEY (beacon_id) REFERENCES BEACON(id),
        FOREIGN KEY (antena_id) REFERENCES ANTENA(id)
    )''')

    if not db_exists:
        cursor.execute("INSERT OR IGNORE INTO ANTENA (id, nome, local) VALUES (1, 'Raspberry1', 'Sala de aula')")
        cursor.execute("INSERT OR IGNORE INTO ANTENA (id, nome, local) VALUES (2, 'Raspberry2', 'Corredor')")
    
    conn.commit()
    conn.close()

def get_or_create_beacon(uuid, nome, mac):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM BEACON WHERE uuid = ?", (uuid,))
    result = cursor.fetchone()
    
    if result:
        beacon_id = result[0]
    else:
        cursor.execute("INSERT INTO BEACON (uuid, nome, mac) VALUES (?, ?, ?)", 
                      (uuid, nome, mac))
        beacon_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return beacon_id

def callback(ch, method, properties, body):
    try:
        message_json = body.decode('utf-8')
        message = json.loads(message_json)
        
        antena_id = message.get('antena')
        datahora = message.get('datahora')
        beacon_uuid = message.get('beacon')
        beacon_nome = message.get('beacon_nome')
        rssi = message.get('rssi')
        mac = message.get('mac')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        beacon_id = get_or_create_beacon(beacon_uuid, beacon_nome, mac)
        
        cursor.execute("INSERT INTO TRACKING (datahora, beacon_id, antena_id, rssi) VALUES (?, ?, ?, ?)",
                      (datahora, beacon_id, antena_id, rssi))
        
        conn.commit()
        conn.close()
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Mensagem Processada com Sucesso: {message_json}")
        
    except Exception as e:
        print(f"Erro ao Processar Mensagem: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)


def main():
    try:
        params = pika.URLParameters(RABBIT_CONFIG)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        channel.exchange_declare(exchange='track_beacons', exchange_type='topic', durable=True)
        channel.queue_declare(queue='tracking')
        channel.queue_bind(exchange='track_beacons', queue='tracking', routing_key='tracking')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue='tracking', on_message_callback=callback)

        print("Aguardando Mensagens...")

        while True:
            channel.connection.process_data_events(time_limit=10)
    except KeyboardInterrupt:
        print("Saiu")

if __name__ == "__main__":
    init_database()
    main()