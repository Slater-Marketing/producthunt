#!/usr/bin/env python3
import undetected_chromedriver as uc
import time

def quick_decodo_test():
    """Quick test of one DECODO endpoint"""
    print("=== Quick DECODO Test ===")
    
    # Test just one endpoint (10001)
    proxy_url = "http://spggrg8ytx:g10LCwaeg3~Vex0eoU@gate.decodo.com:10001"
    
    print(f"Testing: {proxy_url}")
    
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy_url}')
    
    driver = None
    try:
        print("Starting Chrome...")
        driver = uc.Chrome(options=chrome_options, headless=True)
        
        print("Loading test page...")
        driver.get('http://ip.decodo.com/json')
        time.sleep(3)
        
        ip_info = driver.page_source.strip()
        print(f"Response: {ip_info}")
        
        if '"ip"' in ip_info and '"country"' in ip_info:
            print("✅ SUCCESS! Proxy is working!")
            return proxy_url
        else:
            print("❌ Proxy not working - invalid response")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    result = quick_decodo_test()
    if result:
        print(f"\n🎉 Working proxy URL: {result}")
    else:
        print("\n❌ No working proxy found") 