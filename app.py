from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import datetime

app = Flask(__name__)
CORS(app)

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
db = client['github_events']
collection = db['events']

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    try:
        if event_type == 'push':
            author = data['pusher']['name']
            to_branch = data['ref'].split('/')[-1]
            timestamp = datetime.datetime.now().strftime('%dst %B %Y - %I:%M %p UTC')
            message = f'{author} pushed to {to_branch} on {timestamp}'
            
            event_data = {
                'author': author,
                'action': 'PUSH',
                'from_branch': '',
                'to_branch': to_branch,
                'timestamp': timestamp,
                'message': message
            }
            collection.insert_one(event_data)

        elif event_type == 'pull_request':
            if data['action'] == 'opened':
                author = data['pull_request']['user']['login']
                from_branch = data['pull_request']['head']['ref']
                to_branch = data['pull_request']['base']['ref']
                timestamp = datetime.datetime.now().strftime('%dnd %B %Y - %I:%M %p UTC')
                message = f'{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}'
                
                event_data = {
                    'author': author,
                    'action': 'PULL_REQUEST',
                    'from_branch': from_branch,
                    'to_branch': to_branch,
                    'timestamp': timestamp,
                    'message': message
                }
                collection.insert_one(event_data)
            
            elif data['action'] == 'closed' and data['pull_request']['merged']:
                author = data['pull_request']['user']['login']
                from_branch = data['pull_request']['head']['ref']
                to_branch = data['pull_request']['base']['ref']
                timestamp = datetime.datetime.now().strftime('%dnd %B %Y - %I:%M %p UTC')
                message = f'{author} merged branch {from_branch} to {to_branch} on {timestamp}'
                
                event_data = {
                    'author': author,
                    'action': 'MERGE',
                    'from_branch': from_branch,
                    'to_branch': to_branch,
                    'timestamp': timestamp,
                    'message': message
                }
                collection.insert_one(event_data)
    except ServerSelectionTimeoutError:
        return jsonify({"error": "Could not connect to MongoDB."}), 500

    return jsonify({'status': 'success'}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = []
    try:
        for event in collection.find().sort('_id', -1).limit(10):
            events.append({
                'message': event['message']
            })
    except ServerSelectionTimeoutError:
        return jsonify({"error": "Could not connect to MongoDB."}), 500
    return jsonify(events)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)