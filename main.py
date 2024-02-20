from flask import Flask, render_template, request, url_for
import socket
import json
from datetime import datetime

app = Flask(__name__)

# Метод для відправки даних на сервер сокетів
def send_data_to_socket(data):
    # Встановлення з'єднання з сервером сокетів
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        server_address = ('localhost', 5000)  # Адреса сервера сокетів
        s.sendto(json.dumps(data).encode(), server_address)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        # Отримати дані з форми
        username = request.form['username']
        message = request.form['message']
        
        # Формування словника з даними
        data = {
            'timestamp': str(datetime.now()),
            'username': username,
            'message': message
        }
        
        # Відправка даних на сервер сокетів
        send_data_to_socket(data)
        
        # Тут можна проводити обробку введених даних
        return render_template('message.html', username=username, message=message)
    return render_template('message.html')

# Обробка статичних ресурсів
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

# Обробка помилки 404 Not Found
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=3000)
