# 📡 Sistema de Rastreamento de Beacons BLE

Este projeto consiste em um sistema de rastreamento de **beacons BLE** (Bluetooth Low Energy) utilizando antenas baseadas em **Raspberry Pi**. As antenas capturam os sinais Bluetooth dos beacons e enviam esses dados para uma fila de mensageria na nuvem, onde são processados, armazenados em um banco de dados e disponibilizados por meio de uma API.

## 🚀 Funcionalidades

- 📶 Rastreio de dispositivos BLE (beacons) via sinal Bluetooth.
- 🛰️ Antenas baseadas em Raspberry Pi para captura dos sinais.
- ☁️ Envio de dados para um sistema de mensageria (CloudAMQP via RabbitMQ).
- 💾 Processamento e armazenamento dos dados em um banco de dados SQLite.
- 🔗 API RESTful para consulta dos dados rastreados.

## 🛠️ Tecnologias Utilizadas

- **Python** – Linguagem principal do projeto.
- **BLEAK** – Biblioteca para comunicação com dispositivos Bluetooth BLE.
- **Pika** – Cliente Python para RabbitMQ (mensageria).
- **PySerial** – Comunicação com dispositivos seriais, se necessário.
- **Flask** – Framework utilizado para construção da API REST.
- **SQLite** – Banco de dados local e leve para persistência dos dados.

## 📑 Endpoints da API

| Endpoint       | Descrição                            |
|----------------|---------------------------------------|
| `/antenas`     | Lista e consulta as antenas.         |
| `/beacons`     | Lista e consulta os beacons BLE.     |
| `/tracking`    | Consulta os dados de rastreamento.<br>Permite filtros por período, antena ou beacon. |

## 📦 Requisitos

- Python 3.10 ou superior
- Raspberry Pi com Bluetooth habilitado (para as antenas)

### 📜 Dependências (requirements.txt)

```plaintext
asyncio==3.4.3
bleak==0.22.3
pika==1.3.2
serial==0.0.97
pyserial==3.5
flask==3.1.1

```plaintext
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio

```plaintext
python -m venv venv
source venv/bin/activate  # Linux ou MacOS
venv\Scripts\activate     # Windows

```plaintext
pip install -r requirements.txt

