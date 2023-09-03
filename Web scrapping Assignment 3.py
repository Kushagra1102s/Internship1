#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install selenium


# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Ask the user for the product they want to search for
product_name = input("Enter the product you want to search for on Amazon.in: ")

# Create a Chrome WebDriver instance
driver = webdriver.Chrome()

# Navigate to Amazon.in
driver.get("https://www.amazon.in/")

# Find the search input field and enter the product name
search_box = driver.find_element_by_id("twotabsearchtextbox")
search_box.send_keys(product_name)
search_box.send_keys(Keys.RETURN)  # Press Enter

# Wait for the search results to load (you can adjust the time as needed)
driver.implicitly_wait(10)  # Wait for 10 seconds (adjust as needed)

# Get the search results
search_results = driver.find_elements_by_xpath('//div[@data-component-type="s-search-result"]')

# Loop through the search results and print product details
for result in search_results:
    product_title = result.find_element_by_xpath('.//span[@class="a-size-medium a-color-base a-text-normal"]').text
    product_price = result.find_element_by_xpath('.//span[@class="a-price-whole"]').text
    product_currency = result.find_element_by_xpath('.//span[@class="a-price-symbol"]').text
    product_url = result.find_element_by_xpath('.//a[@class="a-link-normal"]').get_attribute("href")

    print(f"Product: {product_title}")
    print(f"Price: {product_currency}{product_price}")
    print(f"URL: {product_url}")
    print()

# Close the web browser
driver.quit()


# In[ ]:


pip install selenium beautifulsoup4 pandas


# In[ ]:


import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

# Function to scrape product details from a search result page
def scrape_product_details(driver, keyword):
    product_data = []
    try:
        # Wait for the page to load
        time.sleep(3)

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all the product containers on the page
        product_containers = soup.find_all('div', class_='s-result-item')

        for container in product_containers:
            try:
                # Extract product details
                brand_name = container.find('span', class_='a-size-base-plus a-color-base').text.strip()
                product_name = container.find('span', class_='a-text-normal').text.strip()
                price = container.find('span', class_='a-price-whole').text.strip()
                return_exchange = container.find('span', class_='a-declarative').text.strip()
                expected_delivery = container.find('span', class_='a-text-bold').text.strip()
                availability = container.find('span', class_='a-size-base a-color-success').text.strip()
                product_url = container.find('a', class_='a-link-normal')['href']

                product_data.append({
                    'Brand Name': brand_name,
                    'Name of the Product': product_name,
                    'Price': price,
                    'Return/Exchange': return_exchange,
                    'Expected Delivery': expected_delivery,
                    'Availability': availability,
                    'Product URL': f'https://www.amazon.in{product_url}',
                })
            except AttributeError:
                # Handle missing data by adding placeholders
                product_data.append({
                    'Brand Name': '-',
                    'Name of the Product': '-',
                    'Price': '-',
                    'Return/Exchange': '-',
                    'Expected Delivery': '-',
                    'Availability': '-',
                    'Product URL': '-',
                })

        return product_data
    except Exception as e:
        print(f"Error scraping product details: {e}")
        return []

# Function to search for a product on Amazon
def search_amazon_product(product_name):
    try:
        driver = webdriver.Chrome()
        driver.get("https://www.amazon.in/")

        # Find the search input field and enter the product name
        search_box = driver.find_element_by_id("twotabsearchtextbox")
        search_box.send_keys(product_name)
        search_box.submit()

        product_data = []

        # Scrape product details from the first 3 pages
        for page in range(3):
            product_data += scrape_product_details(driver, product_name)

            # Navigate to the next page
            try:
                next_button = driver.find_element_by_xpath('//li[@class="a-last"]/a')
                next_button.click()
            except NoSuchElementException:
                break

        return product_data

    except Exception as e:
        print(f"Error searching for the product: {e}")
        return []

    finally:
        driver.quit()

# Main program
if __name__ == "__main__":
    product_name = input("Enter the product you want to search for on Amazon.in: ")
    product_data = search_amazon_product(product_name)

    # Create a DataFrame from the scraped data
    df = pd.DataFrame(product_data)

    # Save the data to a CSV file
    df.to_csv(f"{product_name}_amazon_products.csv", index=False)

    print(f"Scraped {len(df)} products and saved to {product_name}_amazon_products.csv")


# In[ ]:


pip install selenium beautifulsoup4


# In[ ]:


import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import os

# Create a directory to save the downloaded images
if not os.path.exists('downloaded_images'):
    os.makedirs('downloaded_images')

# Function to scrape and download images for a given keyword
def scrape_images(keyword, num_images):
    # Create a Chrome WebDriver instance
    driver = webdriver.Chrome()

    try:
        # Navigate to Google Images
        driver.get("https://www.google.com/imghp")

        # Find the search input field
        search_box = driver.find_element_by_name("q")

        # Enter the keyword and press Enter
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)

        # Wait for the page to load
        time.sleep(3)

        # Scroll down to load more images
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Get the page source after scrolling
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find and download the first num_images images
        img_tags = soup.find_all("img", class_="rg_i")
        count = 0

        for img_tag in img_tags:
            img_url = img_tag.get("src")
            if img_url:
                try:
                    response = requests.get(img_url, stream=True)
                    filename = f"downloaded_images/{keyword}_{count + 1}.jpg"
                    with open(filename, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    count += 1
                    if count >= num_images:
                        break
                except Exception as e:
                    print(f"Error downloading image: {e}")

    except Exception as e:
        print(f"Error scraping images for '{keyword}': {e}")

    finally:
        # Close the web browser
        driver.quit()

# Keywords and the number of images to scrape
keywords = ["fruits", "cars", "Machine Learning", "Guitar", "Cakes"]
num_images = 10

# Scrape images for each keyword
for keyword in keywords:
    print(f"Scraping images for keyword: {keyword}")
    scrape_images(keyword, num_images)

print("Image scraping completed.")


# In[ ]:


import pandas as pd
import requests
from bs4 import BeautifulSoup

# Function to scrape smartphone details from Flipkart
def scrape_smartphone_details(search_query):
    url = f"https://www.flipkart.com/search?q={search_query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("div", class_="_1AtVbE")

        smartphone_data = []
        for product in products:
            try:
                brand_name = product.find("div", class_="_4rR01T").text.strip()
                smartphone_name = product.find("a", class_="IRpwTa").text.strip()
                color = product.find("a", class_="IRpwTa").get("title").split()[-1]
                specifications = product.find_all("li", class_="rgWa7D")

                ram, storage, primary_camera, secondary_camera, display_size, battery_capacity, price = "-", "-", "-", "-", "-", "-", "-"
                for spec in specifications:
                    text = spec.text.strip()
                    if "RAM" in text:
                        ram = text
                    elif "ROM" in text:
                        storage = text
                    elif "Primary Camera" in text:
                        primary_camera = text
                    elif "Secondary Camera" in text:
                        secondary_camera = text
                    elif "Display Size" in text:
                        display_size = text
                    elif "Battery Capacity" in text:
                        battery_capacity = text
                    elif "₹" in text:
                        price = text

                product_url = product.find("a", class_="_1fQZEK")["href"]
                
                smartphone_data.append({
                    "Brand Name": brand_name,
                    "Smartphone Name": smartphone_name,
                    "Colour": color,
                    "RAM": ram,
                    "Storage(ROM)": storage,
                    "Primary Camera": primary_camera,
                    "Secondary Camera": secondary_camera,
                    "Display Size": display_size,
                    "Battery Capacity": battery_capacity,
                    "Price": price,
                    "Product URL": f"https://www.flipkart.com{product_url}",
                })
            except Exception as e:
                print(f"Error scraping product details: {e}")

        return smartphone_data
    else:
        print("Failed to retrieve the Flipkart search results.")
        return []

# Main program
if __name__ == "__main__":
    search_query = input("Enter the smartphone you want to search for on Flipkart: ")
    smartphone_data = scrape_smartphone_details(search_query)

    # Create a DataFrame from the scraped data
    df = pd.DataFrame(smartphone_data)

    # Save the data to a CSV file
    df.to_csv(f"{search_query}_flipkart_smartphones.csv", index=False)

    print(f"Scraped {len(df)} smartphones and saved to {search_query}_flipkart_smartphones.csv")


# In[ ]:


pip install geopy


# In[ ]:


from geopy.geocoders import GoogleV3

def get_coordinates(city_name):
    try:
        geolocator = GoogleV3(api_key='YOUR_GOOGLE_API_KEY')
        location = geolocator.geocode(city_name)
        
        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    city_name = input("Enter the name of the city: ")
    
    coordinates = get_coordinates(city_name)
    
    if coordinates:
        print(f"Coordinates for {city_name}: Latitude {coordinates[0]}, Longitude {coordinates[1]}")
    else:
        print(f"Coordinates for {city_name} not found.")


# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape details of gaming laptops from digit.in
def scrape_gaming_laptops(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the container that holds the laptop details
            laptop_container = soup.find('div', class_='right-container')

            # Extract laptop details
            laptop_name = laptop_container.find('h1', class_='head').text.strip()
            laptop_specs = laptop_container.find_all('div', class_='Specs-Wrap')[1].find_all('div', class_='value')
            laptop_specs = [spec.text.strip() for spec in laptop_specs]

            return {
                'Laptop Name': laptop_name,
                'Processor': laptop_specs[0],
                'OS': laptop_specs[1],
                'Display Size': laptop_specs[2],
                'Resolution': laptop_specs[3],
                'RAM': laptop_specs[4],
                'Weight': laptop_specs[5],
                'Dimension': laptop_specs[6],
                'Graphics Processor': laptop_specs[7],
                'Price': laptop_container.find('div', class_='price').text.strip(),
                'URL': url
            }
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Main program
if __name__ == "__main__":
    url = "https://www.digit.in/top-products/best-gaming-laptops-40.html"
    
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all the links to gaming laptop reviews on the page
        laptop_links = [a['href'] for a in soup.find_all('a', class_='Best-Pick-Image')]

        # List to store laptop details
        laptop_details = []

        # Iterate through the links and scrape laptop details
        for link in laptop_links:
            laptop_detail = scrape_gaming_laptops(link)
            if laptop_detail:
                laptop_details.append(laptop_detail)

        # Create a DataFrame from the scraped data
        df = pd.DataFrame(laptop_details)

        # Save the data to a CSV file
        df.to_csv('gaming_laptops.csv', index=False)

        print(f"Scraped {len(laptop_details)} gaming laptops and saved to gaming_laptops.csv")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape billionaire details from Forbes
def scrape_billionaires(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the table that holds billionaire details
            table = soup.find('table', class_='data')

            # Extract billionaire details from the table
            billionaires = []
            for row in table.find_all('tr')[1:]:
                columns = row.find_all('td')
                rank = columns[0].text.strip()
                name = columns[1].text.strip()
                net_worth = columns[2].text.strip()
                age = columns[3].text.strip()
                citizenship = columns[4].text.strip()
                source = columns[5].text.strip()
                industry = columns[6].text.strip()

                billionaires.append({
                    'Rank': rank,
                    'Name': name,
                    'Net Worth': net_worth,
                    'Age': age,
                    'Citizenship': citizenship,
                    'Source': source,
                    'Industry': industry
                })

            return billionaires
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Main program
if __name__ == "__main__":
    url = "https://www.forbes.com/billionaires/"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the link to the full billionaires list
        list_link = soup.find('a', class_='d-lg-none').get('href')

        # Create the URL for the full list
        full_list_url = f"https://www.forbes.com{list_link}"

        # Scrape billionaire details from the full list URL
        billionaire_details = scrape_billionaires(full_list_url)

        if billionaire_details:
            # Create a DataFrame from the scraped data
            df = pd.DataFrame(billionaire_details)

            # Save the data to a CSV file
            df.to_csv('forbes_billionaires.csv', index=False)

            print(f"Scraped {len(billionaire_details)} billionaires and saved to forbes_billionaires.csv")
        else:
            print("No data scraped.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")


# In[ ]:


import os
import googleapiclient.discovery

# Set your API key here
API_KEY = "YOUR_API_KEY"

# Set the video ID for the YouTube video you want to extract comments from
VIDEO_ID = "YOUR_VIDEO_ID"

# Set the maximum number of comments to retrieve
MAX_RESULTS = 500

# Create a YouTube Data API client
youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

# Function to retrieve video comments
def get_video_comments(video_id, max_results=100):
    comments = []

    # Get video comments in pages of 100 until reaching the desired max_results
    page_token = None
    while True:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            pageToken=page_token
        ).execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "Comment": comment["textDisplay"],
                "Comment Upvotes": comment.get("likeCount", 0),
                "Time Posted": comment["publishedAt"]
            })

            if len(comments) >= max_results:
                return comments

        if "nextPageToken" in response:
            page_token = response["nextPageToken"]
        else:
            break

    return comments

if __name__ == "__main__":
    comments = get_video_comments(VIDEO_ID, max_results=MAX_RESULTS)

    if comments:
        print(f"Total Comments Extracted: {len(comments)}")
        for idx, comment in enumerate(comments):
            print(f"Comment {idx + 1}:")
            print(f"Comment: {comment['Comment']}")
            print(f"Upvotes: {comment['Comment Upvotes']}")
            print(f"Time Posted: {comment['Time Posted']}")
            print("-" * 50)
    else:
        print("No comments extracted.")


# In[ ]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape hostel details
def scrape_hostels(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all the hostel containers
            hostel_containers = soup.find_all('div', class_='property-card')

            # Extract hostel details
            hostels_data = []
            for container in hostel_containers:
                name = container.find('h2', class_='title').text.strip()
                distance = container.find('span', class_='description').text.strip()
                ratings = container.find('div', class_='score orange big').text.strip()
                total_reviews = container.find('div', class_='reviews').text.strip()
                overall_reviews = container.find('div', class_='keyword').text.strip()
                privates_price = container.find('a', class_='price privates from').text.strip()
                dorms_price = container.find('a', class_='price dorms from').text.strip()
                facilities = ', '.join([item.text.strip() for item in container.find_all('li', class_='facility-badge')])
                description = container.find('div', class_='card-body').text.strip()

                hostels_data.append({
                    'Hostel Name': name,
                    'Distance from City Centre': distance,
                    'Ratings': ratings,
                    'Total Reviews': total_reviews,
                    'Overall Reviews': overall_reviews,
                    'Privates Price': privates_price,
                    'Dorms Price': dorms_price,
                    'Facilities': facilities,
                    'Property Description': description
                })

            return hostels_data
        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Main program
if __name__ == "__main__":
    url = "https://www.hostelworld.com/hostels/London/England"

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the total number of pages with hostels
        total_pages = int(soup.find('div', class_='pagination__pages').text.strip().split()[-1])

        # Create a list to store hostel details
        all_hostels_data = []

        # Iterate through all pages and scrape hostel details
        for page_num in range(1, total_pages + 1):
            page_url = f"{url}?page={page_num}"
            hostels_data = scrape_hostels(page_url)
            if hostels_data:
                all_hostels_data.extend(hostels_data)

        # Create a DataFrame from the scraped data
        df = pd.DataFrame(all_hostels_data)

        # Save the data to a CSV file
        df.to_csv('hostelworld_hostels_london.csv', index=False)

        print(f"Scraped {len(all_hostels_data)} hostels and saved to hostelworld_hostels_london.csv")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

