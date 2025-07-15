#!/usr/bin/env python3
"""
Debug script to analyze ProductHunt page structure
This helps identify the correct selectors for scraping.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def analyze_producthunt_page():
    """Analyze ProductHunt page structure"""
    print("Analyzing ProductHunt page structure...")
    
    # Setup Chrome driver
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Load ProductHunt homepage
        print("Loading ProductHunt homepage...")
        driver.get("https://www.producthunt.com/")
        
        # Wait for page to load
        time.sleep(5)
        
        print(f"Page title: {driver.title}")
        print(f"Page URL: {driver.current_url}")
        
        # Check if we're on the right page
        if "Product Hunt" not in driver.title:
            print("⚠️  Warning: Page title doesn't contain 'Product Hunt'")
        
        # Analyze page structure
        print("\nAnalyzing page structure...")
        
        # Look for common product selectors
        selectors_to_check = [
            "[data-test='post-item']",
            "[data-test='post']",
            ".post-item",
            ".post",
            "[class*='post']",
            "[class*='item']",
            "[class*='product']",
            "[class*='card']",
            "article",
            ".feed-item",
            "[data-test*='post']",
            "[data-test*='item']"
        ]
        
        for selector in selectors_to_check:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    print(f"✓ Found {len(elements)} elements with selector: {selector}")
                    if len(elements) > 0:
                        # Show some details about the first element
                        first_element = elements[0]
                        print(f"  First element text preview: {first_element.text[:100]}...")
                        print(f"  First element classes: {first_element.get_attribute('class')}")
                else:
                    print(f"✗ No elements found with selector: {selector}")
            except Exception as e:
                print(f"✗ Error checking selector {selector}: {e}")
        
        # Look for any elements that might contain product information
        print("\nLooking for potential product containers...")
        
        # Check for elements with product-related text
        body_text = driver.find_element(By.TAG_NAME, "body").text
        if "Product Hunt" in body_text:
            print("✓ Found 'Product Hunt' text in page")
        
        # Look for common product-related words
        product_keywords = ["upvote", "vote", "product", "launch", "maker", "tagline"]
        for keyword in product_keywords:
            if keyword.lower() in body_text.lower():
                print(f"✓ Found '{keyword}' in page content")
        
        # Take a screenshot for visual analysis
        screenshot_path = "producthunt_debug_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"\nScreenshot saved as: {screenshot_path}")
        
        # Save page source for analysis
        with open("producthunt_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Page source saved as: producthunt_page_source.html")
        
        # Check for any JavaScript errors or console messages
        console_logs = driver.get_log('browser')
        if console_logs:
            print(f"\nBrowser console logs ({len(console_logs)} entries):")
            for log in console_logs[:5]:  # Show first 5 logs
                print(f"  {log}")
        
        print("\nAnalysis complete!")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    analyze_producthunt_page() 