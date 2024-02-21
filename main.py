from flask import Flask, render_template, request, url_for
import json
from datetime import datetime

app = Flask(__name__)

def save_message(username, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    data = {
        timestamp: {
            "username": username,
            "message": message
        }
    }

    with open("storage/data.json", "a") as json_file:
        json.dump(data, json_file, indent=2)
        json_file.write("\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        username = request.form['username']
        message = request.form['message']
        
        save_message(username, message)
        
        return render_template('message.html', username=username, message=message)
    return render_template('message.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    return url_for('static', filename=filename)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=3000)