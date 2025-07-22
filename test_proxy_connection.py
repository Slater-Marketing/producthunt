#!/usr/bin/env python3
import requests
import undetected_chromedriver as uc
import time
import socket
import subprocess
import sys

def test_proxy_with_requests():
    """Test proxy connection using requests library first"""
    print("=== Testing DECODO Proxy with requests library ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'port': '10001',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    proxies = {
        'http': f'http://{proxy_config["username"]}:{proxy_config["password"]}@{proxy_config["host"]}:{proxy_config["port"]}',
        'https': f'http://{proxy_config["username"]}:{proxy_config["password"]}@{proxy_config["host"]}:{proxy_config["port"]}'
    }
    
    print(f"Proxy URL: {proxies['http']}")
    
    try:
        # Test basic connectivity
        print("Testing basic connectivity...")
        response = requests.get('https://api.ipify.org?format=text', proxies=proxies, timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"IP Address: {response.text.strip()}")
        print("✅ Proxy connection successful with requests")
        return True
    except requests.exceptions.ProxyError as e:
        print(f"❌ Proxy Error: {e}")
        return False
    except requests.exceptions.ConnectTimeout as e:
        print(f"❌ Connection Timeout: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return False

def test_direct_connection():
    """Test direct connection to proxy server"""
    print("\n=== Testing direct connection to proxy server ===")
    
    proxy_host = 'gate.decodo.com'
    proxy_port = 10001
    
    try:
        # Test if we can reach the proxy server
        print(f"Testing connection to {proxy_host}:{proxy_port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((proxy_host, proxy_port))
        sock.close()
        
        if result == 0:
            print("✅ Can reach proxy server")
            return True
        else:
            print(f"❌ Cannot reach proxy server (error code: {result})")
            return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def test_proxy_with_selenium():
    """Test proxy connection using Selenium"""
    print("\n=== Testing DECODO Proxy with Selenium ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'port': '10001',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    proxy_url = f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}"
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    chrome_options.add_argument(f'--proxy-server={proxy_url}')
    
    # Add these options to help with proxy debugging
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    driver = None
    try:
        print("Initializing Chrome WebDriver with proxy...")
        driver = uc.Chrome(options=chrome_options, headless=True)
        
        print("Testing IP address through proxy...")
        driver.get('https://api.ipify.org?format=text')
        time.sleep(5)
        
        ip = driver.page_source.strip()
        print(f"Current IP: {ip}")
        
        # Check if IP is different from your local IP
        local_response = requests.get('https://api.ipify.org?format=text', timeout=10)
        local_ip = local_response.text.strip()
        print(f"Local IP (without proxy): {local_ip}")
        
        if ip != local_ip:
            print("✅ Proxy is working - IP addresses are different")
            return True
        else:
            print("❌ Proxy may not be working - IP addresses are the same")
            return False
            
    except Exception as e:
        print(f"❌ Selenium proxy test failed: {e}")
        return False
    finally:
        if driver:
            driver.quit()

def test_alternative_proxy_formats():
    """Test different proxy URL formats"""
    print("\n=== Testing alternative proxy URL formats ===")
    
    proxy_config = {
        'host': 'gate.decodo.com',
        'port': '10001',
        'username': 'spggrg8ytx',
        'password': 'g10LCwaeg3~Vex0eoU'
    }
    
    # Test different formats
    formats = [
        f"http://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}",
        f"https://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}",
        f"socks5://{proxy_config['username']}:{proxy_config['password']}@{proxy_config['host']}:{proxy_config['port']}",
        f"{proxy_config['host']}:{proxy_config['port']}"
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
            driver.get('https://api.ipify.org?format=text')
            time.sleep(3)
            ip = driver.page_source.strip()
            print(f"  IP: {ip}")
            
            # Check if it's a valid IP (not error page)
            if len(ip.split('.')) == 4 and all(0 <= int(x) <= 255 for x in ip.split('.')):
                print(f"  ✅ Format {i} works!")
                driver.quit()
                return proxy_url
            else:
                print(f"  ❌ Format {i} failed - got: {ip}")
                
        except Exception as e:
            print(f"  ❌ Format {i} failed with error: {e}")
        finally:
            if driver:
                driver.quit()
    
    return None

def main():
    print("DECODO Proxy Connection Test")
    print("=" * 50)
    
    # Test 1: Direct connection
    direct_ok = test_direct_connection()
    
    # Test 2: Requests library
    requests_ok = test_proxy_with_requests()
    
    # Test 3: Selenium
    selenium_ok = test_proxy_with_selenium()
    
    # Test 4: Alternative formats
    working_format = test_alternative_proxy_formats()
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print(f"Direct connection to proxy server: {'✅' if direct_ok else '❌'}")
    print(f"Requests library with proxy: {'✅' if requests_ok else '❌'}")
    print(f"Selenium with proxy: {'✅' if selenium_ok else '❌'}")
    
    if working_format:
        print(f"Working proxy format: {working_format}")
    else:
        print("❌ No working proxy format found")
    
    if not direct_ok:
        print("\n🔧 RECOMMENDATIONS:")
        print("1. Check your internet connection")
        print("2. Verify DECODO credentials are correct")
        print("3. Check if DECODO service is active")
        print("4. Try connecting from a different network")
    
    if direct_ok and not requests_ok:
        print("\n🔧 RECOMMENDATIONS:")
        print("1. Check DECODO credentials")
        print("2. Verify proxy authentication method")
        print("3. Contact DECODO support")

if __name__ == "__main__":
    main() 