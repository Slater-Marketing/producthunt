#!/usr/bin/env python3
"""
Test script for ProductHunt Scraper
This script tests the scraper functionality and verifies all dependencies are installed.
"""

import sys
import importlib

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("Testing dependencies...")
    
    dependencies = [
        'selenium',
        'schedule', 
        'pytz',
        'webdriver_manager'
    ]
    
    missing_deps = []
    
    for dep in dependencies:
        try:
            importlib.import_module(dep)
            print(f"✓ {dep} - OK")
        except ImportError:
            print(f"✗ {dep} - MISSING")
            missing_deps.append(dep)
    
    if missing_deps:
        print(f"\nMissing dependencies: {', '.join(missing_deps)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("\nAll dependencies are installed!")
    return True

def test_chrome_driver():
    """Test if Chrome driver can be initialized"""
    print("\nTesting Chrome driver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Try multiple approaches
        driver = None
        
        # Approach 1: Try with webdriver-manager
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            from selenium.webdriver.chrome.service import Service
            
            driver_path = ChromeDriverManager().install()
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print("✓ Chrome driver initialized successfully (webdriver-manager)")
        except Exception as e1:
            print(f"  WebDriver manager failed: {e1}")
            
            # Approach 2: Try without service
            try:
                driver = webdriver.Chrome(options=chrome_options)
                print("✓ Chrome driver initialized successfully (auto-detection)")
            except Exception as e2:
                print(f"  Auto-detection failed: {e2}")
                
                # Approach 3: Try minimal options
                try:
                    minimal_options = Options()
                    minimal_options.add_argument("--headless")
                    minimal_options.add_argument("--no-sandbox")
                    driver = webdriver.Chrome(options=minimal_options)
                    print("✓ Chrome driver initialized successfully (minimal options)")
                except Exception as e3:
                    print(f"  Minimal options failed: {e3}")
                    raise e3
        
        if driver:
            driver.quit()
            return True
        else:
            return False
        
    except Exception as e:
        print(f"✗ Chrome driver test failed: {e}")
        return False

def test_scraper_import():
    """Test if the scraper module can be imported"""
    print("\nTesting scraper import...")
    
    try:
        from producthunt_scraper import ProductHuntScraper
        print("✓ ProductHuntScraper imported successfully")
        return True
    except Exception as e:
        print(f"✗ Scraper import failed: {e}")
        return False

def test_quick_scrape():
    """Test a quick scrape (just load the page)"""
    print("\nTesting quick scrape...")
    
    try:
        from producthunt_scraper import ProductHuntScraper
        
        scraper = ProductHuntScraper(headless=True)
        
        # Just load the page to test connectivity
        scraper.driver.get("https://www.producthunt.com/")
        
        # Wait a bit for page to load
        import time
        time.sleep(3)
        
        # Check if page loaded
        page_title = scraper.driver.title
        print(f"  Page title: {page_title}")
        
        if "Product Hunt" in page_title:
            print("✓ Successfully loaded ProductHunt page")
            
            # Try to find some content on the page
            try:
                # Look for any content that indicates the page loaded
                body_text = scraper.driver.find_element("tag name", "body").text
                if len(body_text) > 100:  # Page has substantial content
                    print("✓ Page has substantial content")
                    scraper.close()
                    return True
                else:
                    print("✗ Page loaded but has minimal content")
                    scraper.close()
                    return False
            except Exception as e:
                print(f"  Could not check page content: {e}")
                scraper.close()
                return False
        else:
            print(f"✗ Failed to load ProductHunt page (title: {page_title})")
            scraper.close()
            return False
            
    except Exception as e:
        print(f"✗ Quick scrape test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("ProductHunt Scraper Test Suite")
    print("=" * 40)
    
    tests = [
        test_dependencies,
        test_chrome_driver,
        test_scraper_import,
        test_quick_scrape
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The scraper is ready to use.")
        print("\nTo run the scraper:")
        print("  python producthunt_scraper.py")
        print("\nTo run with scheduler:")
        print("  python scheduler.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 