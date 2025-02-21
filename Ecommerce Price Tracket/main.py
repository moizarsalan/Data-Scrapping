from scraper import scrape_prices
from database import save_to_db, get_previous_prices
from notifier import send_alert
from config import PRODUCTS

def main():
    scraped_data = scrape_prices(PRODUCTS)
    previous_prices = get_previous_prices()
    
    for product, details in scraped_data.items():
        old_price = previous_prices.get(product)
        new_price = details["price"]
        
        if old_price and new_price and new_price < old_price:
            send_alert(product, old_price, new_price, details["url"])
    
    save_to_db(scraped_data)
    print("Price tracking completed.")

if __name__ == "__main__":
    main()