#!/usr/bin/env python3
import undetected_chromedriver as uc
import time
import base64

def test_chrome_proxy_auth():
    """Test different Chrome proxy authentication methods"""
    print("=== Testing Chrome Proxy Authentication Methods ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'port': '10001',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    # Method 1: Try with proxy extension approach
    print("\n1. Testing with proxy extension approach...")
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server=http://{proxy_config["host"]}:{proxy_config["port"]}')
    
    # Try to set proxy authentication via preferences
    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.images": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Add proxy authentication via capabilities
    chrome_options.set_capability("proxy", {
        "httpProxy": f"{proxy_config['host']}:{proxy_config['port']}",
        "sslProxy": f"{proxy_config['host']}:{proxy_config['port']}",
        "proxyType": "MANUAL",
        "httpProxyUsername": proxy_config['username'],
        "httpProxyPassword": proxy_config['password']
    })
    
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
    
    # Method 2: Try with different Chrome arguments
    print("\n2. Testing with different Chrome arguments...")
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument(f'--proxy-server=http://{proxy_config["username"]}:{proxy_config["password"]}@{proxy_config["host"]}:{proxy_config["port"]}')
    
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
    result = test_chrome_proxy_auth()
    if result:
        print("\n🎉 Found working Chrome proxy method!")
    else:
        print("\n❌ No working Chrome proxy method found")
        print("We may need to use a different approach or proxy service.") 