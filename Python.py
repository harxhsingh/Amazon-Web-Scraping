import requests
from bs4 import BeautifulSoup
import csv

def get_product_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        products = []
        for product in soup.find_all("div", {"data-component-type": "s-search-result"}):
            product_data = {}
            
            product_name = product.h2.a.span.text.strip()
            product_url = "https://www.amazon.in" + product.h2.a["href"]
            product_price = product.find("span", {"class": "a-price-whole"}).text.strip()
            product_rating = product.find("span", {"class": "a-icon-alt"}).text.strip().split()[0]
            product_reviews = product.find("span", {"class": "a-size-base"}).text.strip().split()[0]
            
            product_data["Product Name"] = product_name
            product_data["Product URL"] = product_url
            product_data["Product Price"] = product_price
            product_data["Rating"] = product_rating
            product_data["Number of Reviews"] = product_reviews
            
            products.append(product_data)
        
        return products
    else:
        print("Error fetching data from:", url)
        return None

def get_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        product_details = {}
        
        product_asin = soup.find("th", text="ASIN").find_next("td").text.strip()
        product_description = soup.find("div", {"id": "productDescription"}).text.strip()
        product_manufacturer = soup.find("a", {"id": "bylineInfo"}).text.strip()
        
        product_details["ASIN"] = product_asin
        product_details["Description"] = product_description
        product_details["Manufacturer"] = product_manufacturer
        
        return product_details
    else:
        print("Error fetching data from:", url)
        return None

if __name__ == "__main__":
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}"
    
    # Scrape 20 pages of product listing pages
    num_pages = 20
    all_products = []
    for page_number in range(1, num_pages + 1):
        url = base_url.format(page_number)
        products = get_product_data(url)
        if products:
            all_products.extend(products)
    
    # Fetch additional details for each product
    for product in all_products:
        product_url = product["Product URL"]
        product_details = get_product_details(product_url)
        if product_details:
            product.update(product_details)
    
    # Export data to CSV
    with open("amazon_products.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Product Name", "Product URL", "Product Price", "Rating", "Number of Reviews", 
                      "Description", "ASIN", "Product Description", "Manufacturer"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_products)
