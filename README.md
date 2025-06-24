
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
- **PySerial** – Comunicação com dispositivos conectados a portas seriais.
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
- Raspberry Pi com Bluetooth habilitado (para as antenas) e conectado a internet

### 📜 Dependências (requirements.txt)

```plaintext
asyncio==3.4.3
bleak==0.22.3
pika==1.3.2
serial==0.0.97
pyserial==3.5
flask==3.1.1
flask-cors==6.0.1
```

## 🏁 Como Executar o Projeto

1. **Clone o repositório:**

```bash
git clone https://github.com/bernardosfz/track_beacons.git
cd track_beacons
```

2. **Crie um ambiente virtual (recomendado):**

```bash
python -m venv venv
source venv/bin/activate  # Linux ou MacOS
venv\Scripts\Activate     # Windows
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure o RabbitMQ:**

- Crie uma conta no [CloudAMQP](https://www.cloudamqp.com/) (serviço RabbitMQ na nuvem).
- Atualize as credenciais no arquivo `config.py` (ou onde estiver definida a configuração com o RabbitMQ).

5. **Execute os scripts:**

- Para **captura dos sinais BLE** e envio para RabbitMQ:

```bash
python main.py
```

- Para **consumir as mensagens do RabbitMQ** e salvar no banco de dados:

```bash
python server.py
```

- Para **iniciar a API Flask:**

```bash
python api.py
```

## 👥 Desenvolvedores

- Bernardo Sozo Fattini  RA: 1134300
- Gabriel Pradegan Orsatto  RA: 1135097
- Henrique Daros Pavão  RA: 1135569
- Jean Folle Vanz  RA: 1134254
- Otavio Augusto Lorenzatto  RA: 1134984

---
