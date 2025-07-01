from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='static')

os.makedirs('donors', exist_ok=True)

@app.route('/')
def index():
    return send_from_directory('.', 'voice_registration.html')

@app.route('/api/donors', methods=['GET', 'POST'])
def handle_donors():
    if request.method == 'POST':
        donor_data = request.json
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f'donor_{timestamp}.json'
        
        with open(f'donors/{filename}', 'w') as f:
            json.dump(donor_data, f, indent=2)
        
        return jsonify({'status': 'success'}), 201
    
    else:
        donors = []
        for filename in os.listdir('donors'):
            if filename.endswith('.json'):
                with open(f'donors/{filename}', 'r') as f:
                    try:
                        donors.append(json.load(f))
                    except json.JSONDecodeError:
                        continue
        
        donors.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return jsonify(donors)

if __name__ == '__main__':
    app.run(debug=True)