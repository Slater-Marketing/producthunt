#!/usr/bin/env python3
import undetected_chromedriver as uc
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_different_approaches():
    """Test different approaches to bypass ProductHunt blocking"""
    print("=== Testing Different Approaches to Bypass ProductHunt Blocking ===\n")
    
    # Test 1: Regular requests library
    print("1. Testing with requests library...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        response = requests.get('https://www.producthunt.com', headers=headers, timeout=10)
        print(f"✅ Requests: Status {response.status_code}, Length: {len(response.text)}")
        if "just a moment" in response.text.lower() or "cloudflare" in response.text.lower():
            print("⚠️  Blocked by Cloudflare")
        else:
            print("✅ Not blocked by Cloudflare")
    except Exception as e:
        print(f"❌ Requests failed: {e}")
    
    # Test 2: Different undetected-chromedriver configurations
    print("\n2. Testing different undetected-chromedriver configs...")
    
    configs = [
        {
            'name': 'Basic undetected',
            'options': ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage']
        },
        {
            'name': 'With stealth options',
            'options': [
                '--headless=new', '--no-sandbox', '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images',
                '--disable-javascript',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        },
        {
            'name': 'With different user agent',
            'options': [
                '--headless=new', '--no-sandbox', '--disable-dev-shm-usage',
                '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ]
        },
        {
            'name': 'Non-headless mode',
            'options': ['--no-sandbox', '--disable-dev-shm-usage', '--window-size=1920,1080']
        }
    ]
    
    for config in configs:
        print(f"\n   Testing: {config['name']}")
        driver = None
        try:
            chrome_options = uc.ChromeOptions()
            for option in config['options']:
                chrome_options.add_argument(option)
            
            driver = uc.Chrome(options=chrome_options, headless='new' in config['options'])
            driver.get('https://www.producthunt.com')
            time.sleep(5)
            
            print(f"   ✅ Page loaded: {driver.title}")
            if "just a moment" in driver.title.lower():
                print("   ⚠️  Blocked by Cloudflare")
            else:
                print("   ✅ Not blocked")
                
            # Check for product elements
            elements = driver.find_elements("css selector", "section[data-test^='post-item-']")
            print(f"   📊 Found {len(elements)} product elements")
            
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        finally:
            if driver:
                driver.quit()
    
    # Test 3: Try different selectors
    print("\n3. Testing different selectors...")
    driver = None
    try:
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = uc.Chrome(options=chrome_options, headless=True)
        driver.get('https://www.producthunt.com')
        time.sleep(5)
        
        selectors_to_try = [
            "section[data-test^='post-item-']",
            "[data-test*='post-item']",
            "section[class*='post']",
            "div[class*='post']",
            "a[href*='/products/']",
            "section[class*='group']",
            "div[class*='group']",
            "article",
            "section"
        ]
        
        for selector in selectors_to_try:
            elements = driver.find_elements("css selector", selector)
            print(f"   '{selector}': {len(elements)} elements")
            
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    test_different_approaches() 