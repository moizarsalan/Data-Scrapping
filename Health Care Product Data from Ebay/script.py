from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_ebay_selenium(max_rows=1000):
    # Set up Chrome options
    options = Options()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    options.add_argument("--log-level=3")  # Suppress logs
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    base_url = "https://www.ebay.com/sch/i.html?_nkw=health+care"
    page = 1
    data = []
    
    while len(data) < max_rows:
        url = f"{base_url}&_pgn={page}"
        driver.get(url)
        time.sleep(3)  # Let page load

        items = driver.find_elements(By.CLASS_NAME, "s-item")
        
        if not items:
            print("No listings found or blocked by eBay.")
            break

        for item in items:
            if len(data) >= max_rows:
                break

            try:
                title = item.find_element(By.CLASS_NAME, "s-item__title").text
                price = item.find_element(By.CLASS_NAME, "s-item__price").text
                
                # Extract stock information if available
                try:
                    stock_info = item.find_element(By.CLASS_NAME, "s-item__availability").text
                except:
                    stock_info = "Not Specified"
                
                # Extract store name if available
                try:
                    store_name = item.find_element(By.CLASS_NAME, "s-item__seller-info-text").text
                except:
                    store_name = "Unknown"
                
                # Extract product condition
                try:
                    condition = item.find_element(By.CLASS_NAME, "SECONDARY_INFO").text
                except:
                    condition = "Not Specified"
                
                # Extract shipping cost & options
                try:
                    shipping = item.find_element(By.CLASS_NAME, "s-item__shipping").text
                except:
                    shipping = "Not Specified"
                
                # Extract item location
                try:
                    location = item.find_element(By.CLASS_NAME, "s-item__location").text
                except:
                    location = "Not Specified"
                
                # Extract number of reviews/ratings
                try:
                    reviews = item.find_element(By.CLASS_NAME, "s-item__reviews-count").text
                except:
                    reviews = "No Reviews"
                
                # Extract seller rating
                try:
                    seller_rating = item.find_element(By.CLASS_NAME, "s-item__seller-info-text").text
                except:
                    seller_rating = "Not Specified"
                
                # Extract discount or offer details
                try:
                    discount = item.find_element(By.CLASS_NAME, "s-item__discount").text
                except:
                    discount = "No Discount"
                
                data.append([title, price, stock_info, store_name, condition, shipping, location, reviews, seller_rating, discount])
            except:
                continue  # Skip items missing details
        
        print(f"Scraped {len(data)} items so far...")
        page += 1
        time.sleep(2)  # Prevent detection

    driver.quit()
    return data

def save_to_csv(data, filename="ebay_healthcare_data.csv"):
    df = pd.DataFrame(data, columns=["Title", "Price", "Stock Info", "Store Name", "Condition", "Shipping", "Location", "Reviews", "Seller Rating", "Discount"])
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    ebay_data = scrape_ebay_selenium()
    save_to_csv(ebay_data)
