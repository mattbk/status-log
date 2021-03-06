#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, render_template
from flask_httpauth import HTTPBasicAuth
import datetime
import humanfriendly

auth = HTTPBasicAuth()

app = Flask(__name__)

statuses = [
    {
        'title': 'app_is_running',
        'color': "green",
        'timestamp': datetime.datetime.now().timestamp(),
        'timestamp_readable': datetime.datetime.now()  
    }
]

@auth.get_password
def get_password(username):
    if username == 'matt':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    
@app.route('/log/new', methods=['POST', 'GET'])
@auth.login_required
def create_status():
    # At least try to clean up user-submitted data
    # https://stackoverflow.com/a/7406369/2152245
    keepcharacters = (' ','.','_')
    safer_title = "".join(c for c in request.args.get("title") if c.isalnum() or c in keepcharacters).rstrip()
    # Limit the length
    safer_title = safer_title[:256]
    
    status = {
        'title': safer_title,
        'color': request.args.get("color"),
        'timestamp': datetime.datetime.now().timestamp(),
        'timestamp_readable': datetime.datetime.now()
    }
    # Add status to list
    statuses.append(status)
    # If list is too big, delete the first item
    # Simple way to prevent someone filling up memory
    if len(statuses) > 1000:
        statuses.pop(0)
    
    return jsonify({'status': status}), 201
    
@app.route('/log/raw', methods=['GET'])
def get_statuses_raw():
    return jsonify({'statuses': statuses[::-1]})
    
@app.route('/log', methods=['GET'])
def get_statuses():
    long_agos = [humanfriendly.format_timespan(datetime.datetime.now().timestamp() - status['timestamp']) for status in statuses[::-1]]
    return render_template("index.html", 
                            statuses = statuses[::-1],
                            long_agos = long_agos)

    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
    
