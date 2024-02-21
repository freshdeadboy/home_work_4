import socket
import json
from datetime import datetime

HOST = 'localhost'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print(f"Socket server is listening on {HOST}:{PORT}")

    while True:
        data, addr = server_socket.recvfrom(1024)
        data_dict = json.loads(data.decode())

        data_dict['timestamp'] = datetime.now().isoformat()

        with open('storage/data.json', 'a') as json_file:
            json.dump(data_dict, json_file, indent=2)
            json_file.write('\n')