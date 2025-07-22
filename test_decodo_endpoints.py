#!/usr/bin/env python3
import requests
import undetected_chromedriver as uc
import time

def test_decodo_endpoints():
    """Test all DECODO endpoints from the user's dashboard"""
    print("=== Testing DECODO Endpoints from Dashboard ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    # All endpoints from the dashboard
    endpoints = [
        {'port': '10001', 'name': 'Endpoint 1'},
        {'port': '10002', 'name': 'Endpoint 2'},
        {'port': '10003', 'name': 'Endpoint 3'},
        {'port': '10004', 'name': 'Endpoint 4'},
        {'port': '10005', 'name': 'Endpoint 5'},
        {'port': '10006', 'name': 'Endpoint 6'},
        {'port': '10007', 'name': 'Endpoint 7'},
        {'port': '10008', 'name': 'Endpoint 8'},
        {'port': '10009', 'name': 'Endpoint 9'},
        {'port': '10010', 'name': 'Endpoint 10'}
    ]
    
    print(f"Testing endpoints for: {proxy_config['username']}@{proxy_config['host']}")
    
    for endpoint in endpoints:
        print(f"\n--- Testing {endpoint['name']} (Port {endpoint['port']}) ---")
        
        # Format: http://username:password@gate.decodo.com:port
        proxy_url = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{endpoint['port']}"
        
        # Test 1: Using requests library
        print("1. Testing with requests...")
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
        print("2. Testing with Selenium...")
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

def test_decodo_alternative_formats():
    """Test alternative formats for the working endpoints"""
    print("\n=== Testing Alternative Formats ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    # Test with port 10001 (first endpoint) using different formats
    port = '10001'
    
    formats = [
        f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{port}",
        f"https://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{port}",
        f"{proxy_config['host']}:{port}",
        f"socks5://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{port}"
    ]
    
    for i, proxy_url in enumerate(formats, 1):
        print(f"\nTesting format {i}: {proxy_url}")
        
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
                print(f"   ✅ Format {i} works!")
                driver.quit()
                return proxy_url
            else:
                print(f"   ❌ Format {i} failed")
                
        except Exception as e:
            print(f"   ❌ Format {i} error: {e}")
        finally:
            if driver:
                driver.quit()
    
    return None

def main():
    print("DECODO Dashboard Endpoints Test")
    print("=" * 50)
    
    # Test all endpoints from dashboard
    working_method = test_decodo_endpoints()
    
    # If no endpoint works, try alternative formats
    if not working_method:
        working_method = test_decodo_alternative_formats()
    
    print("\n" + "=" * 50)
    if working_method:
        print(f"✅ WORKING METHOD FOUND: {working_method}")
        print("\n🔧 NEXT STEPS:")
        print("1. Update the scraper to use this proxy configuration")
        print("2. Test with ProductHunt to ensure it works")
        print("3. Monitor DECODO dashboard for traffic")
        print("4. Consider rotating between endpoints for better performance")
    else:
        print("❌ No working method found")
        print("\n🔧 RECOMMENDATIONS:")
        print("1. Check DECODO dashboard for correct credentials")
        print("2. Verify your subscription is active")
        print("3. Check if you need to whitelist your IP address")
        print("4. Contact DECODO support with your account details")
        print("5. Try using their browser extension to test connectivity")

if __name__ == "__main__":
    main() 