import asyncio
import websockets
import os
import pickle
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from preprocess import preprocess
from urllib.parse import urlparse, parse_qs
import re
import json

connected_clients = set()  # Conjunto para armazenar clientes conectados


class LogHandler(FileSystemEventHandler):
    def __init__(self, model, log_file_path):
        self.model = model
        self.log_file_path = log_file_path
        self.log_position = os.path.getsize(log_file_path)

    async def send_to_clients(self, message):
        # Enviar mensagem para todos os clientes conectados
        for client in connected_clients:
            try:
                await client.send(json.dumps(message))
            except websockets.exceptions.ConnectionClosed:
                connected_clients.remove(client)

    def parse_log(self, log_line):
        """
        Processa uma única linha de log e retorna os campos necessários.
        """
        pattern = r'(\S+) "(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH) ([^ ]+) HTTP/[^"]+" "([^"]+)" "-" "([^"]+)"'
        match = re.search(pattern, log_line)

        if match:
            ip = match.group(1)
            method = match.group(2)
            url = match.group(3)
            accept = match.group(4)
            host = match.group(5)

            parsed_url = urlparse(url)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)
            content = '&'.join([f"{key}={','.join(value)}" for key, value in query_params.items()])

            return {
                "method": method,
                "URL": path,
                "content": content,
                "accept": accept,
                "host": host,
            }
        else:
            raise ValueError(f"Formato de log inválido: {log_line}")

    def on_modified(self, event):
        if event.src_path.endswith("access.log"):
            with open(self.log_file_path, 'r') as f:
                f.seek(self.log_position)
                new_logs = f.readlines()
                self.log_position = f.tell()

                for log_entry in new_logs:
                    log_entry = log_entry.strip()
                    try:
                        log_data = self.parse_log(log_entry)
                        data_preprocessed = preprocess(pd.DataFrame([log_data]), include_label=False)

                        for col in ["method_GET", "method_POST", "method_PUT"]:
                            if col not in data_preprocessed.columns:
                                data_preprocessed[col] = 0

                        prediction = self.model.predict(data_preprocessed)[0]
                        result = {
                            "log": log_entry,
                            "classification": "Malicious" if prediction == 1 else "Non-malicious"
                        }
                        print(result)
                        asyncio.run(self.send_to_clients(result))
                    except ValueError as e:
                        print(f"Log inválido ignorado: {e}")
                    except Exception as e:
                        print(f"Erro inesperado ao processar o log: {e}")


async def websocket_server(websocket):
    connected_clients.add(websocket)
    print(f"Novo cliente conectado")

    try:
        while True:
            await asyncio.sleep(1)
    except websockets.exceptions.ConnectionClosed:
        print("Cliente desconectado")
        connected_clients.remove(websocket)


def monitor_logs_with_websocket(log_path, model_path):
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    log_handler = LogHandler(model, log_path)
    observer = Observer()
    observer.schedule(log_handler, path=os.path.dirname(log_path), recursive=False)
    observer.start()

    print(f"Monitoring logs at {log_path}...")

    async def start_websocket_server():
        async with websockets.serve(websocket_server, "localhost", 8765):
            print("WebSocket Server iniciado na porta 8765...")
            await asyncio.Future()

    try:
        asyncio.run(start_websocket_server())
    except KeyboardInterrupt:
        print("Interrompendo monitoramento...")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    log_path = "/var/log/apache2/access.log"
    model_path = "../models/random_forest"
    monitor_logs_with_websocket(log_path, model_path)
