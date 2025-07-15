#!/usr/bin/env python3
"""
Chrome Driver Troubleshooting Script
This script helps fix common Chrome driver issues on Windows.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_chrome_installation():
    """Check if Chrome is installed and get its version"""
    print("Checking Chrome installation...")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✓ Chrome found at: {path}")
            chrome_found = True
            
            # Get Chrome version
            try:
                result = subprocess.run([path, "--version"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"  Version: {result.stdout.strip()}")
            except Exception as e:
                print(f"  Could not get version: {e}")
    
    if not chrome_found:
        print("✗ Chrome not found in common locations")
        print("Please install Google Chrome from: https://www.google.com/chrome/")
        return False
    
    return True

def clear_webdriver_cache():
    """Clear webdriver-manager cache"""
    print("\nClearing webdriver-manager cache...")
    
    cache_paths = [
        os.path.expanduser("~/.wdm"),
        os.path.expanduser("~/.cache/selenium"),
        os.path.expanduser("~/.cache/webdriver")
    ]
    
    for cache_path in cache_paths:
        if os.path.exists(cache_path):
            try:
                shutil.rmtree(cache_path, ignore_errors=True)
                print(f"✓ Cleared cache: {cache_path}")
            except Exception as e:
                print(f"✗ Failed to clear cache {cache_path}: {e}")
        else:
            print(f"  Cache not found: {cache_path}")

def install_chrome_driver():
    """Install Chrome driver using webdriver-manager"""
    print("\nInstalling Chrome driver...")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Force download of latest driver
        driver_path = ChromeDriverManager().install()
        print(f"✓ Chrome driver installed at: {driver_path}")
        
        # Verify the driver file exists and is executable
        if os.path.exists(driver_path):
            print(f"✓ Driver file exists: {driver_path}")
            return True
        else:
            print(f"✗ Driver file not found: {driver_path}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to install Chrome driver: {e}")
        return False

def test_chrome_driver():
    """Test if Chrome driver works"""
    print("\nTesting Chrome driver...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        
        if "Google" in driver.title:
            print("✓ Chrome driver test successful")
            driver.quit()
            return True
        else:
            print("✗ Chrome driver test failed - page not loaded correctly")
            driver.quit()
            return False
            
    except Exception as e:
        print(f"✗ Chrome driver test failed: {e}")
        return False

def main():
    """Main troubleshooting function"""
    print("Chrome Driver Troubleshooting")
    print("=" * 40)
    
    # Step 1: Check Chrome installation
    if not check_chrome_installation():
        print("\nPlease install Google Chrome first.")
        return False
    
    # Step 2: Clear cache
    clear_webdriver_cache()
    
    # Step 3: Install Chrome driver
    if not install_chrome_driver():
        print("\nFailed to install Chrome driver.")
        return False
    
    # Step 4: Test Chrome driver
    if not test_chrome_driver():
        print("\nChrome driver test failed.")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 Chrome driver troubleshooting completed successfully!")
    print("You can now run the ProductHunt scraper.")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 