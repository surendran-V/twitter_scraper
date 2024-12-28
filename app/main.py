from flask import Flask, render_template, jsonify, request
from scraper import scrape_twitter_trends, save_to_mongodb
from config import Config
import os

# Validate configuration on startup
Config.validate_config()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    trends = scrape_twitter_trends()
    record = save_to_mongodb(trends)
    
    if not record:
        return jsonify({"error": "Failed to fetch or save trends"}), 500
    
    # Extract client IP address
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    record['client_ip'] = client_ip
    
    return jsonify(record)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
