import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import csv

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# The URL you want to scrape
url = "https://playboard.co/en/search?q=tech"
driver.get(url)

# Wait for the page to load initially
time.sleep(2)

# Function to check for email addresses in a text
def contains_email(text):
    return any(word.endswith("@") and "." in word for word in text.split())

# Create a list to store scraped data
# scraped_data = []

# Save the scraped data to a CSV file
csv_filename = "scraped_data.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Title", "Description"])


    # Scroll to the end of the page
    while True:
        # Scroll down to trigger infinite scrolling
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

        # Wait for 2 seconds to load more content
        time.sleep(6)

        # Get the page source
        page_source = driver.page_source
        # print(page_source)

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all elements with class "channels"
        channels = soup.find(class_="channels")

        channels_list = channels.find_all(class_="list")

        for channel in channels_list:
            # Find elements with class "channel-cell" or "list__item"
            channel_items = channel.find_all(class_="channel-cell")
            
            for item in channel_items:
                # Find the div with class "meta"
                meta_div = item.find(class_="meta")
                if meta_div:
                    # Find the h2 tag
                    h2_tag = meta_div.find('h2')
                    if h2_tag:
                        h2_text = h2_tag.get_text(strip=True)
                        # print(h2_text)
                    
                    # Find the div with class "desc"
                    desc_div = item.find(class_="desc")
                    if desc_div:
                        desc_text = desc_div.get_text(strip=True)
                        # print(desc_text)
                        
                    csv_writer.writerow([h2_text, desc_text])

        # Check if you have reached the end of the page
        current_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(20)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == current_height:
            break

    # Close the web browser
    driver.close()

print(f"Data has been scraped and saved to {csv_filename}")
