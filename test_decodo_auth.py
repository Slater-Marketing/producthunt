#!/usr/bin/env python3
import requests
import undetected_chromedriver as uc
import time
import base64

def test_decodo_auth_methods():
    """Test different DECODO authentication methods"""
    print("=== Testing DECODO Authentication Methods ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'port': '10001',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    # Method 1: Basic auth in URL (current method)
    print("\n1. Testing Basic Auth in URL...")
    proxy_url1 = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}"
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy_url1}')
    
    driver = None
    try:
        driver = uc.Chrome(options=chrome_options, headless=True)
        driver.get('https://api.ipify.org?format=text')
        time.sleep(3)
        ip = driver.page_source.strip()
        print(f"   IP: {ip}")
        if len(ip.split('.')) == 4 and all(0 <= int(x) <= 255 for x in ip.split('.')):
            print("   ✅ Method 1 works!")
            driver.quit()
            return proxy_url1
        else:
            print("   ❌ Method 1 failed")
    except Exception as e:
        print(f"   ❌ Method 1 error: {e}")
    finally:
        if driver:
            driver.quit()
    
    # Method 2: Proxy with separate auth extension
    print("\n2. Testing Proxy with Auth Extension...")
    proxy_url2 = f"{proxy_config['host']}:{proxy_config['port']}"
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy_url2}')
    
    # Add proxy auth extension
    auth_string = base64.b64encode(f"{proxy_config['username']}:{proxy_config['password']}".encode()).decode()
    chrome_options.add_argument(f'--proxy-auth={auth_string}')
    
    driver = None
    try:
        driver = uc.Chrome(options=chrome_options, headless=True)
        driver.get('https://api.ipify.org?format=text')
        time.sleep(3)
        ip = driver.page_source.strip()
        print(f"   IP: {ip}")
        if len(ip.split('.')) == 4 and all(0 <= int(x) <= 255 for x in ip.split('.')):
            print("   ✅ Method 2 works!")
            driver.quit()
            return proxy_url2
        else:
            print("   ❌ Method 2 failed")
    except Exception as e:
        print(f"   ❌ Method 2 error: {e}")
    finally:
        if driver:
            driver.quit()
    
    # Method 3: SOCKS5 proxy
    print("\n3. Testing SOCKS5 Proxy...")
    proxy_url3 = f"socks5://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}"
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy_url3}')
    
    driver = None
    try:
        driver = uc.Chrome(options=chrome_options, headless=True)
        driver.get('https://api.ipify.org?format=text')
        time.sleep(3)
        ip = driver.page_source.strip()
        print(f"   IP: {ip}")
        if len(ip.split('.')) == 4 and all(0 <= int(x) <= 255 for x in ip.split('.')):
            print("   ✅ Method 3 works!")
            driver.quit()
            return proxy_url3
        else:
            print("   ❌ Method 3 failed")
    except Exception as e:
        print(f"   ❌ Method 3 error: {e}")
    finally:
        if driver:
            driver.quit()
    
    # Method 4: Check if DECODO uses a different port or protocol
    print("\n4. Testing alternative DECODO configurations...")
    
    # Try different ports that DECODO might use
    alternative_ports = ['10000', '10002', '10003', '8080', '3128']
    
    for port in alternative_ports:
        print(f"   Testing port {port}...")
        proxy_url4 = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{port}"
        
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f'--proxy-server={proxy_url4}')
        
        driver = None
        try:
            driver = uc.Chrome(options=chrome_options, headless=True)
            driver.get('https://api.ipify.org?format=text')
            time.sleep(3)
            ip = driver.page_source.strip()
            print(f"     IP: {ip}")
            if len(ip.split('.')) == 4 and all(0 <= int(x) <= 255 for x in ip.split('.')):
                print(f"     ✅ Port {port} works!")
                driver.quit()
                return proxy_url4
            else:
                print(f"     ❌ Port {port} failed")
        except Exception as e:
            print(f"     ❌ Port {port} error: {e}")
        finally:
            if driver:
                driver.quit()
    
    return None

def test_decodo_documentation():
    """Test based on common DECODO documentation patterns"""
    print("\n=== Testing DECODO Documentation Patterns ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'port': '10001',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    # Method 5: DECODO often uses session-based authentication
    print("\n5. Testing Session-based Authentication...")
    
    # First, try to authenticate with DECODO's auth endpoint
    try:
        auth_url = f"http://{proxy_config['host']}:{proxy_config['port']}/auth"
        auth_data = {
            'username': proxy_config['username'],
            'password': proxy_config['password']
        }
        
        response = requests.post(auth_url, json=auth_data, timeout=10)
        print(f"   Auth response: {response.status_code}")
        print(f"   Auth content: {response.text[:200]}")
        
    except Exception as e:
        print(f"   Auth endpoint error: {e}")
    
    # Method 6: Try without authentication (DECODO might use IP whitelist)
    print("\n6. Testing without authentication...")
    proxy_url6 = f"{proxy_config['host']}:{proxy_config['port']}"
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy_url6}')
    
    driver = None
    try:
        driver = uc.Chrome(options=chrome_options, headless=True)
        driver.get('https://api.ipify.org?format=text')
        time.sleep(3)
        ip = driver.page_source.strip()
        print(f"   IP: {ip}")
        if len(ip.split('.')) == 4 and all(0 <= int(x) <= 255 for x in ip.split('.')):
            print("   ✅ No auth works!")
            driver.quit()
            return proxy_url6
        else:
            print("   ❌ No auth failed")
    except Exception as e:
        print(f"   ❌ No auth error: {e}")
    finally:
        if driver:
            driver.quit()
    
    return None

def main():
    print("DECODO Authentication Test")
    print("=" * 50)
    
    # Test standard methods
    working_method = test_decodo_auth_methods()
    
    if not working_method:
        # Test documentation patterns
        working_method = test_decodo_documentation()
    
    print("\n" + "=" * 50)
    if working_method:
        print(f"✅ WORKING METHOD FOUND: {working_method}")
        print("\n🔧 NEXT STEPS:")
        print("1. Update the scraper to use this authentication method")
        print("2. Test with ProductHunt to ensure it works")
    else:
        print("❌ No working authentication method found")
        print("\n🔧 RECOMMENDATIONS:")
        print("1. Check DECODO documentation for correct authentication method")
        print("2. Verify your DECODO account is active and has residential proxy access")
        print("3. Contact DECODO support with your credentials")
        print("4. Check if DECODO requires a different endpoint or protocol")

if __name__ == "__main__":
    main() 