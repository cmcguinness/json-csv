from flask import Flask, render_template, request, jsonify
import pandas as pd
from io import StringIO
import socket
import os


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))  # Bind to an available port provided by the host.
        return s.getsockname()[1]  # Return the port number assigned.

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert_csv_to_json', methods=['POST'])
def convert_csv_to_json():
    csv_data = request.form['csv_data']
    csv_buffer = StringIO(csv_data)
    df = pd.read_csv(csv_buffer)
    return df.to_json(orient='records')

@app.route('/convert_json_to_csv', methods=['POST'])
def convert_json_to_csv():
    json_data = request.form['json_data']
    json_buffer = StringIO(json_data)
    df = pd.read_json(json_buffer)
    csv_data = df.to_csv(index=False)
    return csv_data

if __name__ == '__main__':
    port = find_free_port()
    os.system('open http://127.0.0.1:' + str(port))
    app.run(port=port, debug=False)
