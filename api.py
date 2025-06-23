from flask import Flask, jsonify, request
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = 'tracking_database.db'

def conectar_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/antenas', methods=['GET'])
def listar_antenas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, local FROM ANTENA")
    rows = cursor.fetchall()
    conn.close()

    antenas = [dict(row) for row in rows]
    return jsonify(antenas)

@app.route('/beacons', methods=['GET'])
def listar_beacons():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, uuid, mac FROM BEACON")
    rows = cursor.fetchall()
    conn.close()

    beacons = [dict(row) for row in rows]
    return jsonify(beacons)

@app.route('/tracking', methods=['GET'])
def get_tracking():
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    antena_id = request.args.get('antena_id')
    beacon_id = request.args.get('beacon_id')

    query = "SELECT id, datahora, beacon_id, antena_id, rssi FROM TRACKING WHERE 1=1"
    params = []

    if data_inicio:
        query += " AND DATE(datahora) >= DATE(?)"
        params.append(data_inicio)
    if data_fim:
        query += " AND DATE(datahora) <= DATE(?)"
        params.append(data_fim)
    if antena_id:
        query += " AND antena_id = ?"
        params.append(antena_id)
    if beacon_id:
        query += " AND beacon_id = ?"
        params.append(beacon_id)

    query += " ORDER BY datahora DESC"

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    tracking = [dict(row) for row in rows]
    return jsonify(tracking)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API Online"})

if __name__ == '__main__':
    app.run(debug=True)
