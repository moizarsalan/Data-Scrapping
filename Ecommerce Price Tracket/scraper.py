import requests
from bs4 import BeautifulSoup
from config import HEADERS

def scrape_prices(products):
    scraped_data = {}

    for site, url in products.items():
        try:
            print(f"Fetching data from {site}...")  # Debugging log
            response = requests.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            price = None  # Default price as None
            
            if site == "Amazon":
                price_tag = soup.find("span", class_="a-price-whole")
                price = price_tag.text.strip() if price_tag else None
            
            elif site == "eBay":
                price_tag = soup.find("span", class_="s-item__price")
                price = price_tag.text.strip() if price_tag else None
            
            elif site == "Walmart":
                price_tag = soup.find("span", class_="price-characteristic")
                price = price_tag["content"] if price_tag and "content" in price_tag.attrs else None
            
            elif site == "AliExpress":
                price_tag = soup.find("span", class_="product-price-value")
                price = price_tag.text.strip() if price_tag else None

            # Convert price to float if valid
            if price:
                try:
                    price = float(price.replace("$", "").replace(",", ""))
                except ValueError:
                    print(f"Error converting price for {site}: {price}")
                    price = None
            
            scraped_data[site] = {
                "price": price,
                "url": url
            }

        except requests.RequestException as e:
            print(f"Error fetching {site}: {e}")
            scraped_data[site] = {"price": None, "url": url}

    return scraped_data