#!/usr/bin/env python3
import undetected_chromedriver as uc
import time
import os

def test_decodo_extension_method():
    """Test DECODO with different authentication methods"""
    print("=== Testing DECODO with Extension Method ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'port': '10001',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    # Method 1: Try without authentication in URL (let Chrome handle it)
    print("\n1. Testing without auth in URL...")
    proxy_url1 = f"http://{proxy_config['host']}:{proxy_config['port']}"
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy_url1}')
    
    # Add proxy authentication via command line
    chrome_options.add_argument(f'--proxy-auth={proxy_config["username"]}:{proxy_config["password"]}')
    
    driver = None
    try:
        print("Starting Chrome...")
        driver = uc.Chrome(options=chrome_options, headless=True)
        
        print("Loading test page...")
        driver.get('http://ip.decodo.com/json')
        time.sleep(5)
        
        ip_info = driver.page_source.strip()
        print(f"Response: {ip_info}")
        
        if '"ip"' in ip_info and '"country"' in ip_info:
            print("✅ SUCCESS! Proxy is working!")
            return True
        else:
            print("❌ Proxy not working - invalid response")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if driver:
            driver.quit()
    
    # Method 2: Try with different port
    print("\n2. Testing with port 7000 (from DECODO docs)...")
    proxy_url2 = f"http://{proxy_config['host']}:7000"
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy_url2}')
    chrome_options.add_argument(f'--proxy-auth={proxy_config["username"]}:{proxy_config["password"]}')
    
    driver = None
    try:
        print("Starting Chrome...")
        driver = uc.Chrome(options=chrome_options, headless=True)
        
        print("Loading test page...")
        driver.get('http://ip.decodo.com/json')
        time.sleep(5)
        
        ip_info = driver.page_source.strip()
        print(f"Response: {ip_info}")
        
        if '"ip"' in ip_info and '"country"' in ip_info:
            print("✅ SUCCESS! Proxy is working!")
            return True
        else:
            print("❌ Proxy not working - invalid response")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if driver:
            driver.quit()
    
    return False

if __name__ == "__main__":
    result = test_decodo_extension_method()
    if result:
        print("\n🎉 Found working proxy method!")
    else:
        print("\n❌ No working proxy method found") 