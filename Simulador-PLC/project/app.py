from flask import Flask, jsonify, render_template
from threading import Thread
import random
import time
import modbus_tk.modbus_tcp as modbus_tcp
import modbus_tk.defines as cst

# Configuração inicial dos registradores para os dois PLCs
registers_plc1 = [0.0] * 10
registers_plc2 = [0.0] * 10

# Função para atualizar os registradores mais lentamente para os índices 0 a 4
def slow_update(registers):
    for i in range(5):
        registers[i] = round(random.uniform(16.0, 35.0), 2)

# Função para atualizar os registradores a cada 2 segundos
def update_registers(slave1, slave2):
    counter = 0  # Contador para alternar a atualização lenta

    while True:
        # Atualizar registradores do PLC 1
        if counter % 5 == 0:  # Atualiza os índices 0 a 4 mais devagar
            slow_update(registers_plc1)
        for i in range(5, 10):  # Atualiza os índices 5 a 9 normalmente
            registers_plc1[i] = round(random.uniform(0.0, 100.0), 2)
        slave1.set_values('holding_registers', 0, [int(v * 100) for v in registers_plc1])

        # Atualizar registradores do PLC 2
        if counter % 5 == 0:  # Atualiza os índices 0 a 4 mais devagar
            slow_update(registers_plc2)
        for i in range(5, 10):  # Atualiza os índices 5 a 9 normalmente
            registers_plc2[i] = round(random.uniform(50.0, 150.0), 2)
        slave2.set_values('holding_registers', 0, [int(v * 100) for v in registers_plc2])

        counter += 1
        time.sleep(2)

# Configuração do servidor Modbus-TCP para dois PLCs
def start_modbus_servers():
    # Configurar o servidor PLC 1
    server_plc1 = modbus_tcp.TcpServer(port=502)
    server_plc1.start()
    slave_plc1 = server_plc1.add_slave(1)
    slave_plc1.add_block('holding_registers', cst.HOLDING_REGISTERS, 0, 10)

    # Configurar o servidor PLC 2
    server_plc2 = modbus_tcp.TcpServer(port=503)
    server_plc2.start()
    slave_plc2 = server_plc2.add_slave(1)
    slave_plc2.add_block('holding_registers', cst.HOLDING_REGISTERS, 0, 10)

    # Iniciar a atualização dos registradores
    update_registers(slave_plc1, slave_plc2)

# Frontend usando Flask
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registers/plc1")
def get_registers_plc1():
    return jsonify(registers_plc1)

@app.route("/registers/plc2")
def get_registers_plc2():
    return jsonify(registers_plc2)

if __name__ == "__main__":
    # Iniciar Modbus em uma thread separada
    Thread(target=start_modbus_servers).start()
    # Iniciar o servidor Flask
    app.run(host="0.0.0.0", port=5000)
