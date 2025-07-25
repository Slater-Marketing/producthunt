import time
import json
import csv
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
import undetected_chromedriver as uc
import random
import warnings
warnings.filterwarnings("ignore", message="could not detect version_main")
import requests

class ProductHuntScraper:
    def __init__(self, headless=True):
        self.base_url = "https://www.producthunt.com"
        self.today_url = self.base_url  # Use homepage for today's products
        self.products = []
        self.request_count = 0
        self.last_request_time = 0
        self.setup_logging()
        self.setup_driver(headless)
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('producthunt_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_driver(self, headless=True):
        """Setup Chrome WebDriver with appropriate options using undetected-chromedriver"""
        chrome_options = uc.ChromeOptions()
        if headless:
            chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        # Server optimization options
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")  # Don't load images to save memory
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--memory-pressure-off")
        chrome_options.add_argument("--max_old_space_size=1024")  # 1GB for 2GB server
        
        try:
            self.driver = uc.Chrome(options=chrome_options, headless=headless)
            # Set longer timeouts for server environments
            self.driver.set_page_load_timeout(60)
            self.driver.implicitly_wait(10)
            self.logger.info("Undetected Chrome WebDriver initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize undetected Chrome WebDriver: {e}")
            raise
    
    def rate_limit_delay(self):
        """Add rate limiting delay between requests"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Ensure minimum 2 seconds between requests
        min_delay = 2
        if time_since_last < min_delay:
            sleep_time = min_delay - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
        
        # Add exponential backoff every 10 requests
        if self.request_count % 10 == 0:
            backoff_time = min(30, 2 ** (self.request_count // 10))  # Max 30 seconds
            self.logger.info(f"Rate limiting: waiting {backoff_time} seconds after {self.request_count} requests")
            time.sleep(backoff_time)
    
    def clean_url(self, url):
        """Remove ?ref=producthunt and similar tracking params from a URL."""
        if not url or not isinstance(url, str):
            return url
        try:
            parsed = urlparse(url)
            # Remove 'ref=producthunt' and 'utm_source=producthunt' and similar
            query = [(k, v) for k, v in parse_qsl(parsed.query) if k not in ["ref", "utm_source"] or v.lower() != "producthunt"]
            cleaned = urlunparse(parsed._replace(query=urlencode(query)))
            return cleaned
        except Exception:
            return url

    def combine_fields(self, ph_val, site_val):
        """Combine two fields according to preference rules, robust to None and whitespace."""
        ph_val = (ph_val or '').strip()
        site_val = (site_val or '').strip()
        if not ph_val and not site_val:
            return ""
        if site_val and not ph_val:
            return site_val
        if ph_val and not site_val:
            return ph_val
        if ph_val.lower() == site_val.lower():
            return ph_val
        # Both are known and different, prefer producthunt
        return ph_val

    def get_todays_products(self):
        """Scrape all products from today's ProductHunt homepage and their website/social/email links in parallel, resuming from CSV if present, and send each to a webhook."""
        try:
            self.logger.info(f"Starting to scrape products from: {self.today_url}")
            # Resume logic: read existing CSV and collect already-scraped URLs and rows
            filename = f"producthunt_products_{datetime.now().strftime('%Y%m%d')}.csv"
            already_scraped_urls = set()
            existing_products = []
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if 'url' in row and row['url']:
                            already_scraped_urls.add(row['url'])
                        existing_products.append(row)
                self.logger.info(f"Loaded {len(already_scraped_urls)} already-scraped products from CSV.")
            
            # Load the homepage with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    self.rate_limit_delay()
                    self.driver.get(self.today_url)
                    self.logger.info(f"Page loaded successfully (attempt {attempt + 1})")
                    break
                except Exception as e:
                    self.logger.warning(f"Failed to load page (attempt {attempt + 1}): {e}")
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(2)
            
            time.sleep(5)  # Longer wait for page to load
            self.logger.info(f"Page title: {self.driver.title}")
            
            # Click the 'See all of today's products' button if present
            try:
                see_all_btn = self.driver.find_element(By.XPATH, "//span[contains(text(), \"See all of today's products\")]")
                self.logger.info("Found 'See all of today's products' button, clicking it...")
                see_all_btn.click()
                time.sleep(2)  # Wait for products to load
            except Exception as e:
                self.logger.info("'See all of today's products' button not found or already expanded.")
            
            # Scroll to load all products via infinite scroll
            self._scroll_to_load_all_products()
            
            # Use the new selector for product listings
            product_elements = self.driver.find_elements(By.CSS_SELECTOR, "section[data-test^='post-item-']")
            self.logger.info(f"Found {len(product_elements)} product elements with new selector.")
            
            if not product_elements:
                # Take a screenshot for debugging
                screenshot_path = f"producthunt_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                self.driver.save_screenshot(screenshot_path)
                self.logger.error(f"No product elements found. Screenshot saved as: {screenshot_path}")
                self.logger.error(f"Page source preview: {self.driver.page_source[:500]}...")
                raise Exception("No product elements found on the page")

            def scrape_product(element):
                try:
                    product_data = self._extract_product_data_new(element)
                    if product_data:
                        # Skip if already scraped
                        if product_data.get('url') in already_scraped_urls:
                            self.logger.info(f"Skipping already-scraped product: {product_data.get('url')}")
                            return None
                        # Step 1: Scrape ProductHunt product page for website, socials, email
                        ph_links = self._get_links_from_product_page_separate_driver(product_data.get("url"))
                        product_data.update(ph_links)
                        # Step 2: Scrape the external website for socials, email
                        site_links = self._get_links_from_external_website(product_data.get("website_url"))
                        product_data.update(site_links)
                        # Clean all URLs
                        for key in ["url", "website_url", "ph_instagram", "ph_linkedin_company", "ph_linkedin_personal", "ph_x", "ph_facebook", "site_instagram", "site_linkedin_company", "site_linkedin_personal", "site_x", "site_facebook"]:
                            if key in product_data and product_data[key]:
                                product_data[key] = self.clean_url(product_data[key])
                        return product_data
                except Exception as e:
                    self.logger.warning(f"Failed to extract product data: {e}")
                    return None

            # Process products in batches to avoid memory issues on server
            batch_size = 30  # Process 30 products at a time (2GB server)
            results = []
            webhook_url = "https://services.leadconnectorhq.com/hooks/knCxBYvGSI3aHQOSBd35/webhook-trigger/28e182ff-acc2-4d86-8ca6-e10990c103ee"
            
            for i in range(0, len(product_elements), batch_size):
                batch = product_elements[i:i + batch_size]
                self.logger.info(f"Processing batch {i//batch_size + 1}/{(len(product_elements) + batch_size - 1)//batch_size} ({len(batch)} products)")
                
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future_to_element = {executor.submit(scrape_product, el): el for el in batch}
                    for future in as_completed(future_to_element):
                        data = future.result()
                        if data:
                            results.append(data)
                            # Combine fields for webhook
                            combined = dict(data)
                            combined['instagram'] = self.combine_fields(data.get('ph_instagram'), data.get('site_instagram'))
                            combined['linkedin_company'] = self.combine_fields(data.get('ph_linkedin_company'), data.get('site_linkedin_company'))
                            combined['linkedin_personal'] = self.combine_fields(data.get('ph_linkedin_personal'), data.get('site_linkedin_personal'))
                            combined['x'] = self.combine_fields(data.get('ph_x'), data.get('site_x'))
                            combined['facebook'] = self.combine_fields(data.get('ph_facebook'), data.get('site_facebook'))
                            combined['email'] = self.combine_fields(data.get('ph_email'), data.get('site_email'))
                            # Send to webhook
                            try:
                                resp = requests.post(webhook_url, json=combined, timeout=15)
                                if resp.status_code == 200:
                                    self.logger.info(f"Sent product to webhook: {data.get('url')}")
                                else:
                                    self.logger.warning(f"Webhook failed for {data.get('url')}: {resp.status_code}")
                            except Exception as e:
                                self.logger.warning(f"Webhook error for {data.get('url')}: {e}")
                            # Add to existing products for CSV
                            existing_products.append(combined)
                
                # Memory cleanup between batches
                self.logger.info(f"Completed batch {i//batch_size + 1}, processed {len(results)} total products")
                time.sleep(10)  # Longer pause between batches to avoid rate limiting
            
            self.products = existing_products + results
            self.logger.info(f"Successfully processed {len(self.products)} products (webhook mode)")
            return self.products
            
        except Exception as e:
            self.logger.error(f"Error scraping products: {e}")
            raise
    
    def _scroll_to_load_all_products(self):
        """Scroll down to load all products via infinite scroll - optimized for server environments"""
        self.logger.info("Scrolling to load all products...")
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_attempts = 15  # Increased for server environments
        products_before = 0
        
        while scroll_attempts < max_attempts:
            try:
                # Scroll down in smaller increments for server environments
                current_height = self.driver.execute_script("return window.pageYOffset")
                self.driver.execute_script(f"window.scrollTo(0, {current_height + 800});")
                time.sleep(5)  # Longer wait for server environments and rate limiting
                
                # Calculate new scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                
                # Check current product count
                product_elements = self.driver.find_elements(By.CSS_SELECTOR, "section[data-test^='post-item-']")
                current_products = len(product_elements)
                
                self.logger.info(f"Scroll attempt {scroll_attempts + 1}: {current_products} products loaded")
                
                # If no new products loaded and no height change, increment attempts
                if new_height == last_height and current_products == products_before:
                    scroll_attempts += 1
                else:
                    scroll_attempts = 0
                    last_height = new_height
                    products_before = current_products
                
                # Stop if we've loaded enough products or hit max attempts
                if current_products > 300:  # Higher limit for 2GB server
                    self.logger.info(f"Loaded {current_products} products, stopping scroll")
                    break
                    
                # Memory management: clear some elements periodically
                if scroll_attempts % 5 == 0:
                    self.driver.execute_script("window.gc();")  # Force garbage collection
                    
            except Exception as e:
                self.logger.warning(f"Error during scroll attempt {scroll_attempts + 1}: {e}")
                scroll_attempts += 1
                time.sleep(2)
        
        self.logger.info("Finished scrolling")
    
    def _extract_product_data_new(self, element):
        """Extract product data from a new-style homepage product section"""
        try:
            # Product name
            try:
                name_a = element.find_element(By.CSS_SELECTOR, "a[data-test^='post-name-']")
                name = name_a.text.strip()
                # Remove leading number and dot (e.g., '19. daily backlinks' -> 'daily backlinks')
                name = re.sub(r'^\d+\.\s*', '', name)
                product_url = name_a.get_attribute("href")
                if product_url and product_url.startswith("/"):
                    product_url = f"https://www.producthunt.com{product_url}"
            except Exception:
                name = ""
                product_url = ""
            
            # Tagline (the next <a> after the name link)
            try:
                tagline_a = element.find_elements(By.CSS_SELECTOR, "a")
                tagline = ""
                for a in tagline_a:
                    if a != name_a and "/products/" in a.get_attribute("href"):
                        tagline = a.text.strip()
                        break
            except Exception:
                tagline = ""
            
            # Image
            try:
                img = element.find_element(By.CSS_SELECTOR, "img")
                image_url = img.get_attribute("src")
            except Exception:
                image_url = ""
            
            # Topics (all <a> inside the tag list)
            try:
                topics = []
                taglist = element.find_elements(By.CSS_SELECTOR, "[data-sentry-component='TagList'] a")
                for t in taglist:
                    topics.append(t.text.strip())
            except Exception:
                topics = []
            
            # Upvotes (from the vote button)
            try:
                upvote_btn = element.find_element(By.CSS_SELECTOR, "button[data-test='vote-button'] p")
                upvotes = upvote_btn.text.strip()
            except Exception:
                upvotes = "0"
            
            product_data = {
                "name": name,
                "tagline": tagline,
                "url": product_url,
                "image_url": image_url,
                "topics": topics,
                "upvotes": upvotes,
                "scraped_at": datetime.now().isoformat(),
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            return product_data
        except Exception as e:
            self.logger.warning(f"Error extracting product data (new): {e}")
            return None
    
    def _get_links_from_product_page_separate_driver(self, product_url):
        """Open a new undetected Chrome WebDriver to visit the product page and extract website URL, social and email links."""
        result = {"website_url": "", "ph_instagram": "", "ph_linkedin_company": "", "ph_linkedin_personal": "", "ph_x": "", "ph_facebook": "", "ph_email": ""}
        # Social links to skip (ProductHunt's own)
        skip_socials = [
            "facebook.com/producthunt",
            "x.com/producthunt",
            "twitter.com/producthunt",
            "linkedin.com/company/producthunt",
            "instagram.com/producthunt"
        ]
        try:
            chrome_options = uc.ChromeOptions()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            driver = None
            try:
                driver = uc.Chrome(options=chrome_options, headless=True)
                driver.get(product_url)
                time.sleep(random.uniform(5, 15))  # Longer random delay to avoid rate limiting
                # Website URL
                try:
                    website_btn = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-test='visit-website-button']"))
                    )
                    result["website_url"] = website_btn.get_attribute("href")
                except Exception:
                    result["website_url"] = ""
                # Social and email links
                all_links = driver.find_elements(By.CSS_SELECTOR, "a[href]")
                for a in all_links:
                    href = a.get_attribute("href")
                    if not href:
                        continue
                    href_lower = href.lower()
                    if any(s in href_lower for s in skip_socials):
                        continue
                    if "instagram.com" in href_lower and not result["ph_instagram"]:
                        result["ph_instagram"] = href
                    elif "linkedin.com" in href_lower:
                        if "/company/" in href_lower and not result["ph_linkedin_company"]:
                            result["ph_linkedin_company"] = href
                        elif "/company/" not in href_lower and not result["ph_linkedin_personal"]:
                            result["ph_linkedin_personal"] = href
                    elif ("twitter.com" in href_lower or "x.com" in href_lower) and not result["ph_x"]:
                        result["ph_x"] = href
                    elif "facebook.com" in href_lower and not result["ph_facebook"]:
                        result["ph_facebook"] = href
                    elif href_lower.startswith("mailto:") and not result["ph_email"]:
                        result["ph_email"] = href.replace("mailto:", "")
                # Also search for visible emails in the page text
                if not result["ph_email"]:
                    page_text = driver.page_source
                    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", page_text)
                    if email_match:
                        result["ph_email"] = email_match.group(0)
            finally:
                if driver:
                    driver.quit()
        except Exception as e:
            self.logger.warning(f"Failed to visit product page {product_url}: {e}")
        return result

    def _get_links_from_external_website(self, website_url):
        """Open a new undetected Chrome WebDriver to visit the external website and extract social and email links."""
        if not website_url or not website_url.startswith("http"):
            return {"site_instagram": "", "site_linkedin_company": "", "site_linkedin_personal": "", "site_x": "", "site_facebook": "", "site_email": ""}
        result = {"site_instagram": "", "site_linkedin_company": "", "site_linkedin_personal": "", "site_x": "", "site_facebook": "", "site_email": ""}
        # Social links to skip (ProductHunt's own)
        skip_socials = [
            "facebook.com/producthunt",
            "x.com/producthunt",
            "twitter.com/producthunt",
            "linkedin.com/company/producthunt",
            "instagram.com/producthunt"
        ]
        try:
            chrome_options = uc.ChromeOptions()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            
            driver = None
            try:
                driver = uc.Chrome(options=chrome_options, headless=True)
                driver.get(website_url)
                time.sleep(random.uniform(5, 15))  # Longer random delay to avoid rate limiting
                all_links = driver.find_elements(By.CSS_SELECTOR, "a[href]")
                for a in all_links:
                    href = a.get_attribute("href")
                    if not href:
                        continue
                    href_lower = href.lower()
                    if any(s in href_lower for s in skip_socials):
                        continue
                    if "instagram.com" in href_lower and not result["site_instagram"]:
                        result["site_instagram"] = href
                    elif "linkedin.com" in href_lower:
                        if "/company/" in href_lower and not result["site_linkedin_company"]:
                            result["site_linkedin_company"] = href
                        elif "/company/" not in href_lower and not result["site_linkedin_personal"]:
                            result["site_linkedin_personal"] = href
                    elif ("twitter.com" in href_lower or "x.com" in href_lower) and not result["site_x"]:
                        result["site_x"] = href
                    elif "facebook.com" in href_lower and not result["site_facebook"]:
                        result["site_facebook"] = href
                    elif href_lower.startswith("mailto:") and not result["site_email"]:
                        result["site_email"] = href.replace("mailto:", "")
                # Also search for visible emails in the page text
                if not result["site_email"]:
                    page_text = driver.page_source
                    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", page_text)
                    if email_match:
                        result["site_email"] = email_match.group(0)
            finally:
                if driver:
                    driver.quit()
        except Exception as e:
            self.logger.warning(f"Failed to visit external website {website_url}: {e}")
        return result
    
    def save_to_json(self, filename=None):
        """Save scraped products to JSON file"""
        if not filename:
            filename = f"producthunt_products_{datetime.now().strftime('%Y%m%d')}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.products, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Products saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {e}")
    
    def save_to_csv(self, filename=None):
        """Save scraped products to CSV file"""
        if not filename:
            filename = f"producthunt_products_{datetime.now().strftime('%Y%m%d')}.csv"
        
        try:
            if not self.products:
                self.logger.warning("No products to save")
                return
            
            fieldnames = self.products[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.products)
            self.logger.info(f"Products saved to {filename}")
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {e}")
    
    def close(self):
        """Close the WebDriver"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            self.logger.info("WebDriver closed")

def main():
    """Main function to run the scraper"""
    scraper = None
    try:
        scraper = ProductHuntScraper(headless=True)
        products = scraper.get_todays_products()
        
        if products:
            scraper.save_to_json()
            scraper.save_to_csv()
            print(f"Successfully scraped {len(products)} products from ProductHunt")
        else:
            print("No products found")
            
    except Exception as e:
        print(f"Error running scraper: {e}")
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main() 