# test_debug.py
from app.scraper import TwitterScraper
import traceback

def test_scraping_debug():
    try:
        print("Starting debug test...")
        print("Initializing scraper...")
        scraper = TwitterScraper()
        
        print("\nAttempting to get trending topics...")
        trends = scraper.get_trending_topics()
        
        print("\nSuccess! Retrieved trends:")
        for i in range(1, 6):
            print(f"Trend {i}: {trends[f'nameoftrend{i}']}")
            
    except Exception as e:
        print("\nError occurred:")
        print(str(e))
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_scraping_debug()