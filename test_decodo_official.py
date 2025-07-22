#!/usr/bin/env python3
import requests
import undetected_chromedriver as uc
import time

def test_decodo_official_format():
    """Test DECODO using their official documentation format"""
    print("=== Testing DECODO Official Format ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'port': '7000',  # DECODO docs use port 7000
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    # Official DECODO format from their docs
    proxy_url = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}"
    
    print(f"Testing proxy URL: {proxy_url}")
    
    # Test 1: Using requests (from their Python example)
    print("\n1. Testing with requests library...")
    try:
        response = requests.get('http://ip.decodo.com/json', 
                              proxies={'http': proxy_url, 'https': proxy_url}, 
                              timeout=10)
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
        if response.status_code == 200:
            print("   ✅ Requests test successful!")
        else:
            print("   ❌ Requests test failed")
    except Exception as e:
        print(f"   ❌ Requests error: {e}")
    
    # Test 2: Using Selenium
    print("\n2. Testing with Selenium...")
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy_url}')
    
    driver = None
    try:
        driver = uc.Chrome(options=chrome_options, headless=True)
        driver.get('http://ip.decodo.com/json')
        time.sleep(5)
        
        ip_info = driver.page_source.strip()
        print(f"   Response: {ip_info}")
        
        # Check if we got a valid JSON response
        if '"ip"' in ip_info and '"country"' in ip_info:
            print("   ✅ Selenium test successful!")
            driver.quit()
            return proxy_url
        else:
            print("   ❌ Selenium test failed - invalid response")
            
    except Exception as e:
        print(f"   ❌ Selenium error: {e}")
    finally:
        if driver:
            driver.quit()
    
    return None

def test_decodo_alternative_ports():
    """Test DECODO with alternative ports from their documentation"""
    print("\n=== Testing Alternative DECODO Ports ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    # Try different ports that DECODO might use
    ports_to_test = ['7000', '10001', '10000', '10002', '8080', '3128']
    
    for port in ports_to_test:
        print(f"\nTesting port {port}...")
        proxy_url = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{port}"
        
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f'--proxy-server={proxy_url}')
        
        driver = None
        try:
            driver = uc.Chrome(options=chrome_options, headless=True)
            driver.get('http://ip.decodo.com/json')
            time.sleep(3)
            
            ip_info = driver.page_source.strip()
            print(f"   Response: {ip_info[:200]}...")
            
            if '"ip"' in ip_info and '"country"' in ip_info:
                print(f"   ✅ Port {port} works!")
                driver.quit()
                return proxy_url
            else:
                print(f"   ❌ Port {port} failed")
                
        except Exception as e:
            print(f"   ❌ Port {port} error: {e}")
        finally:
            if driver:
                driver.quit()
    
    return None

def test_decodo_without_auth():
    """Test if DECODO uses IP whitelist authentication"""
    print("\n=== Testing DECODO without authentication (IP whitelist) ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'port': '7000'
    }
    
    proxy_url = f"{proxy_config['host']}:{proxy_config['port']}"
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy_url}')
    
    driver = None
    try:
        driver = uc.Chrome(options=chrome_options, headless=True)
        driver.get('http://ip.decodo.com/json')
        time.sleep(3)
        
        ip_info = driver.page_source.strip()
        print(f"Response: {ip_info}")
        
        if '"ip"' in ip_info and '"country"' in ip_info:
            print("✅ IP whitelist authentication works!")
            driver.quit()
            return proxy_url
        else:
            print("❌ IP whitelist authentication failed")
            
    except Exception as e:
        print(f"❌ IP whitelist error: {e}")
    finally:
        if driver:
            driver.quit()
    
    return None

def main():
    print("DECODO Official Documentation Test")
    print("=" * 50)
    
    # Test 1: Official format with port 7000
    working_method = test_decodo_official_format()
    
    # Test 2: Alternative ports
    if not working_method:
        working_method = test_decodo_alternative_ports()
    
    # Test 3: IP whitelist
    if not working_method:
        working_method = test_decodo_without_auth()
    
    print("\n" + "=" * 50)
    if working_method:
        print(f"✅ WORKING METHOD FOUND: {working_method}")
        print("\n🔧 NEXT STEPS:")
        print("1. Update the scraper to use this proxy configuration")
        print("2. Test with ProductHunt to ensure it works")
        print("3. Monitor DECODO dashboard for traffic")
    else:
        print("❌ No working method found")
        print("\n🔧 RECOMMENDATIONS:")
        print("1. Check DECODO dashboard for correct credentials")
        print("2. Verify your subscription is active")
        print("3. Check if you need to whitelist your IP address")
        print("4. Contact DECODO support with your account details")

if __name__ == "__main__":
    main() 