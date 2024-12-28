# Twitter Trending Topics Scraper

This project is a web application for scraping trending topics on Twitter. It utilizes Selenium for web scraping, MongoDB for data storage, and Flask for the web interface. The application also integrates a proxy service for secure and anonymous web scraping.

## Features

- Scrapes trending topics from Twitter using Selenium.
- Stores scraped trends in a MongoDB database.
- Web interface to trigger scraping and display results.
- Secure handling of sensitive credentials using environment variables.
- Proxy support for secure and anonymous web requests.

## Project Structure

```
├── app
|  ├── config.py
|  ├── database.py
|  ├── main.py
|  ├── scraper.py
|  ├── __init__.py
|  └── __pycache__
├── proxy_test.py
├── README.md
├── requirements.txt
├── setup_db.js
├── static
|  └── css
├── templates
|  └── index.html
└── venv
   ├── Include
   ├── Lib
   ├── pyvenv.cfg
   └── Scripts

directory: 9 file: 11
```

## Requirements

- Python 3.8+
- MongoDB
- Google Chrome
- ChromeDriver
- A valid Twitter account for scraping

## Installation

1. Clone the repository:
 ```bash
 git clone https://github.com/surendran-V/twitter_scraper.git
 cd twitter_scraper
 ```
2. Set up a virtual environment:
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Set up environment variables: Create a .env file in the app directory and add the following:
```
TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password
PROXYMESH_USERNAME=your_proxymesh_username
PROXYMESH_PASSWORD=your_proxymesh_password
PROXYMESH_HOST=your_proxymesh_host
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=trending_topics
COLLECTION_NAME=trends
```
5. Start MongoDB: Ensure MongoDB is running locally or update the MONGODB_URI in your .env file to point to your database instance.
6. Install ChromeDriver: Download the appropriate ChromeDriver for your Chrome version and update the system PATH or specify its path in the scraper code.

## Usage 
1. Start the Flask server:
```
python main.py
```
2. Access the web interface: Open your browser and go to http://localhost:5000.
3. Trigger scraping: Click on the "Scrape" button to fetch the latest trending topics on Twitter.

## Dependencies
- Selenium: Web scraping
- Flask: Web framework
- pymongo: MongoDB interaction
- dotenv: Environment variable management
