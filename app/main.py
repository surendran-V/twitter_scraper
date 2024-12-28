# app/main.py
from flask import jsonify, render_template
from app import create_app
from app.scraper import TwitterScraper
from app.database import Database

app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scrape')
def scrape():
    try:
        scraper = TwitterScraper()
        trends_data = scraper.get_trending_topics()
        
        db = Database()
        db.insert_trends(trends_data)
        db.close()
        
        return jsonify(trends_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)