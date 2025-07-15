import schedule
import time
import logging
from datetime import datetime
import pytz
from producthunt_scraper import ProductHuntScraper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_scraper():
    """Run the ProductHunt scraper"""
    logger.info("Starting scheduled ProductHunt scraper run")
    scraper = None
    
    try:
        scraper = ProductHuntScraper(headless=True)
        products = scraper.get_todays_products()
        
        if products:
            scraper.save_to_json()
            scraper.save_to_csv()
            logger.info(f"Successfully scraped {len(products)} products from ProductHunt")
        else:
            logger.warning("No products found")
            
    except Exception as e:
        logger.error(f"Error running scraper: {e}")
    finally:
        if scraper:
            scraper.close()
        logger.info("Scheduled scraper run completed")

def schedule_daily_run():
    """Schedule the scraper to run daily at 11pm PST"""
    # Schedule the job to run at 11:00 PM PST every day
    schedule.every().day.at("23:00").do(run_scraper)
    
    logger.info("Scheduled ProductHunt scraper to run daily at 11:00 PM PST")
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

def run_once():
    """Run the scraper once immediately"""
    logger.info("Running scraper once")
    run_scraper()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--run-once":
        run_once()
    else:
        schedule_daily_run() 