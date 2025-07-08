from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import datetime

# --- Helper Functions ---

def format_date_with_ordinal(dt):
    """
    Formats a datetime object into a string with the correct ordinal for the day.
    Example: 1st, 2nd, 3rd, 4th.
    """
    day = dt.day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    
    return dt.strftime(f'%d{suffix} %B %Y - %I:%M %p UTC')

# --- Flask App Setup ---

app = Flask(__name__)
CORS(app)

# --- Database Configuration ---

# Connect to the local MongoDB instance.
# serverSelectionTimeoutMS is set to handle cases where the DB is not immediately available.
client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
db = client['github_events']
collection = db['events']

# --- Webhook Endpoint ---

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Receives webhook events from GitHub, processes them,
    and stores them in the MongoDB database.
    """
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    now = datetime.datetime.utcnow()

    try:
        # --- Push Event ---
        if event_type == 'push':
            author = data.get('pusher', {}).get('name', 'Unknown')
            to_branch = data.get('ref', '').split('/')[-1]
            formatted_timestamp = format_date_with_ordinal(now)
            message = f'{author} pushed to {to_branch} on {formatted_timestamp}'
            
            event_data = {
                'author': author,
                'action': 'PUSH',
                'to_branch': to_branch,
                'timestamp': formatted_timestamp,
                'message': message,
                'created_at': now
            }
            collection.insert_one(event_data)

        # --- Pull Request Event ---
        elif event_type == 'pull_request':
            pull_request = data.get('pull_request', {})
            
            # --- Opened Pull Request ---
            if data.get('action') == 'opened':
                author = pull_request.get('user', {}).get('login', 'Unknown')
                from_branch = pull_request.get('head', {}).get('ref', 'Unknown')
                to_branch = pull_request.get('base', {}).get('ref', 'Unknown')
                formatted_timestamp = format_date_with_ordinal(now)
                message = f'{author} submitted a pull request from {from_branch} to {to_branch} on {formatted_timestamp}'
                
                event_data = {
                    'author': author,
                    'action': 'PULL_REQUEST',
                    'from_branch': from_branch,
                    'to_branch': to_branch,
                    'timestamp': formatted_timestamp,
                    'message': message,
                    'created_at': now
                }
                collection.insert_one(event_data)
            
            # --- Merged Pull Request ---
            elif data.get('action') == 'closed' and pull_request.get('merged'):
                author = pull_request.get('user', {}).get('login', 'Unknown')
                from_branch = pull_request.get('head', {}).get('ref', 'Unknown')
                to_branch = pull_request.get('base', {}).get('ref', 'Unknown')
                formatted_timestamp = format_date_with_ordinal(now)
                message = f'{author} merged branch {from_branch} to {to_branch} on {formatted_timestamp}'
                
                event_data = {
                    'author': author,
                    'action': 'MERGE',
                    'from_branch': from_branch,
                    'to_branch': to_branch,
                    'timestamp': formatted_timestamp,
                    'message': message,
                    'created_at': now
                }
                collection.insert_one(event_data)
    except ServerSelectionTimeoutError:
        return jsonify({"error": "Could not connect to MongoDB."}), 500

    return jsonify({'status': 'success'}), 200

@app.route('/events', methods=['GET'])
def get_events():
    """
    Provides a list of recent events.
    Accepts an optional 'since' query parameter in ISO format
    to fetch only events newer than the given timestamp.
    """
    events = []
    query = {}
    
    # Check for the 'since' parameter to fetch events incrementally
    since_timestamp_str = request.args.get('since')
    if since_timestamp_str:
        try:
            # Convert the ISO format string back to a datetime object
            since_timestamp = datetime.datetime.fromisoformat(since_timestamp_str.replace('Z', '+00:00'))
            query['created_at'] = {'$gt': since_timestamp}
        except ValueError:
            # Handle potential malformed timestamp string
            return jsonify({"error": "Invalid timestamp format."}), 400

    try:
        # Fetch events, sorted by creation time descending
        for event in collection.find(query).sort('created_at', -1).limit(10):
            events.append({
                'message': event['message'],
                # Send the timestamp in a standardized ISO format
                'created_at': event['created_at'].isoformat()
            })
    except ServerSelectionTimeoutError:
        return jsonify({"error": "Could not connect to MongoDB."}), 500
    
    return jsonify(events)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)