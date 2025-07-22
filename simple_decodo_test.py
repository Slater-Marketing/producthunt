#!/usr/bin/env python3
import requests
import time

def simple_decodo_test():
    """Simple test to check DECODO connection"""
    print("=== Simple DECODO Connection Test ===")
    
    # Test direct connection to DECODO server
    print("1. Testing direct connection to DECODO server...")
    try:
        response = requests.get('http://gate.decodo.com:10001', timeout=10)
        print(f"✅ Can reach DECODO server: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot reach DECODO server: {e}")
    
    # Test with basic auth
    print("\n2. Testing with basic auth...")
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
    
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10)
        print(f"✅ Proxy working with requests: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Proxy not working with requests: {e}")
    
    return False

if __name__ == "__main__":
    result = simple_decodo_test()
    if result:
        print("\n🎉 DECODO proxy works with requests library!")
        print("The issue is with Chrome/Selenium proxy support.")
    else:
        print("\n❌ DECODO proxy doesn't work at all.") 