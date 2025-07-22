#!/usr/bin/env python3
import undetected_chromedriver as uc
import time
import random

def test_proxy_and_page():
    """Test proxy connection and check ProductHunt page content"""
    
    # DECODO Proxy configuration
    proxy_config = {
        'host': 'gate.decodo.com',
        'port': '10001',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    proxy_url = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}"
    
    print(f"Testing proxy: {proxy_config['host']}:{proxy_config['port']}")
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument(f'--proxy-server={proxy_url}')
    
    driver = None
    try:
        print("Initializing Chrome WebDriver...")
        driver = uc.Chrome(options=chrome_options, headless=True)
        
        # Test proxy by checking IP
        print("Testing proxy connection...")
        driver.get('https://api.ipify.org?format=text')
        time.sleep(3)
        ip = driver.page_source.strip()
        print(f"Current IP: {ip}")
        
        # Test ProductHunt
        print("Loading ProductHunt...")
        driver.get('https://www.producthunt.com')
        time.sleep(10)  # Wait longer for page to load
        
        print(f"Page title: {driver.title}")
        print(f"Page URL: {driver.current_url}")
        
        # Check if we're being blocked
        if "just a moment" in driver.title.lower() or "cloudflare" in driver.page_source.lower():
            print("⚠️  WARNING: Page appears to be blocked by Cloudflare")
        
        # Look for any product-related elements
        print("\nSearching for product elements...")
        
        # Try different selectors
        selectors_to_try = [
            "section[data-test^='post-item-']",
            "[data-test*='post-item']",
            "section[class*='post']",
            "div[class*='post']",
            "a[href*='/products/']",
            "section[class*='group']",
            "div[class*='group']"
        ]
        
        for selector in selectors_to_try:
            elements = driver.find_elements("css selector", selector)
            print(f"Selector '{selector}': Found {len(elements)} elements")
            if elements:
                print(f"  First element text: {elements[0].text[:100]}...")
        
        # Check for the "See all of today's products" button
        try:
            button = driver.find_element("css selector", "span:contains('See all of today')")
            print("✅ Found 'See all of today's products' button")
        except:
            print("❌ 'See all of today's products' button not found")
        
        # Save page source for debugging
        with open('debug_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("Page source saved to debug_page_source.html")
        
        # Take screenshot
        driver.save_screenshot('debug_screenshot.png')
        print("Screenshot saved to debug_screenshot.png")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_proxy_and_page() 