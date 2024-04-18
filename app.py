from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

app = Flask(__name__)

def scrape_google_local_services(city,search_key,scrape_page):
    driver = webdriver.Chrome()

    # Open the Google Local Services page
    driver.get('https://www.google.com/localservices/prolist?g2lbs=AIQllVzWSYspFtzaywPV9jv6ozuwdPjt7hfraOfChGkHnMWRs6jF0EN0JnmLVAxCXczEjUzv4oHOVvTL6BdV-38uYjJ1IChxr0ZEAtiL7qHihksvHmIrYX9YXjZaRJZM3RoWbXTEIRAz&hl=en-IN&gl=in&ssta=1&q=digital%20marketing%20agency&oq=digital%20marketing%20agency&slp=MgA6HENoTUlwNk9mdTl6a2hBTVZCUS1EQXgzU1FBV19SAggCYACSAbgCCg0vZy8xMWg1N2sxNTMxCg0vZy8xMWJ3NjlyemhwCg0vZy8xMXFwbTVoY2YyCg0vZy8xMWprNHZ2NXQ1Cg0vZy8xMXM2MXN3ZDg3Cg0vZy8xMXZqaG1tbGZtCg0vZy8xMWZzdm01XzF5Cg0vZy8xMWxjZnE0eV9yCg0vZy8xMWtqajcycnQzCg0vZy8xMXJzYnIzcnc5Cg0vZy8xMWozNDQ4OHE4Cg0vZy8xMXNzd3BzZnAzCg0vZy8xMWYzam15M2puCg0vZy8xMWhmNHJfcThyCg0vZy8xMW4xNTB6aHNoCg0vZy8xMWM2N3dtOHRmCg0vZy8xMWRkeGJ6cmNsCg0vZy8xMWg0X2xzMHc0Cg0vZy8xMWoyZnA0bWIyCg0vZy8xMXY1eDM0OGpzEgQSAggBEgQKAggBmgEGCgIXGRAA&src=2&serdesk=1&sa=X&ved=2ahUKEwiurZS73OSEAxX91TgGHYHWCWYQjGp6BAgiEAE&scp=ChVnY2lkOm1hcmtldGluZ19hZ2VuY3kSVxISCRcp3KaMReA7EXyOXMDrZ7gEGhIJYxUdQVlO4DsRQrA4CSlYRf4iFVN1cmF0LCBHdWphcmF0IDM5NTAwNioUDfIgoAwVUZVqKx3Upq4MJZ0nfiswARoYZGlnaXRhbCBtYXJrZXRpbmcgYWdlbmN5IhhkaWdpdGFsIG1hcmtldGluZyBhZ2VuY3kqEE1hcmtldGluZyBhZ2VuY3k%3D')  

    # Find the search input element and input the search query
    search_input = driver.find_element(By.CSS_SELECTOR, 'input[class="MDhB7"]')
    search_input.clear()  # Clear any existing text in the search input
    search_input.send_keys(search_key, Keys.ENTER)

    time.sleep(2)  # Wait for the results to load
    data = []
    def scrape_page():
    # Collect data
        nonlocal data 
        elements = driver.find_elements(By.CSS_SELECTOR, '[class="NwqBmc"]')
        for element in elements:
            item = {}
            try:
                driver.execute_script("arguments[0].scrollIntoView();", element)
                item['name'] = element.find_element(By.CSS_SELECTOR, '.rgnuSb').text.strip()
                item['rating'] = element.find_element(By.CSS_SELECTOR, '.OJbIQb').text
                item['addresses'] = element.find_element(By.XPATH, './/span[2][contains(@class, "hGz87c")]').text
                item['phones'] = element.find_element(By.XPATH, './/span[3][contains(@class, "hGz87c")]').text
                data.append(item)
            except Exception as e:
                print("Error occurred:", e)

    
    scrape_page()
    while True:   
        try:
            button = driver.find_elements(By.XPATH, '//button[@aria-label="Next"]')[1]
            #driver.execute_script("arguments[0].click();", button)
            button.click()
            time.sleep(2)
            scrape_page()
        except:
            break
    
    driver.quit()  # Quit the driver after scraping
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/scraped", methods=['POST'])
def scraped():
    if request.method == "POST":
        city = request.form['city']
        search_key = request.form['search_key']
        scrape_page = request.form.get('scrape_page')
        search_key += " " + city  # Concatenate city name to the search key
        results = scrape_google_local_services(city, search_key,scrape_page)
        return render_template('scraped_data.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)


'''
driver = webdriver.Chrome()

driver.get('https://www.google.com/localservices/prolist?g2lbs=AIQllVzWSYspFtzaywPV9jv6ozuwdPjt7hfraOfChGkHnMWRs6jF0EN0JnmLVAxCXczEjUzv4oHOVvTL6BdV-38uYjJ1IChxr0ZEAtiL7qHihksvHmIrYX9YXjZaRJZM3RoWbXTEIRAz&hl=en-IN&gl=in&ssta=1&q=digital%20marketing%20agency&oq=digital%20marketing%20agency&slp=MgA6HENoTUlwNk9mdTl6a2hBTVZCUS1EQXgzU1FBV19SAggCYACSAbgCCg0vZy8xMWg1N2sxNTMxCg0vZy8xMWJ3NjlyemhwCg0vZy8xMXFwbTVoY2YyCg0vZy8xMWprNHZ2NXQ1Cg0vZy8xMXM2MXN3ZDg3Cg0vZy8xMXZqaG1tbGZtCg0vZy8xMWZzdm01XzF5Cg0vZy8xMWxjZnE0eV9yCg0vZy8xMWtqajcycnQzCg0vZy8xMXJzYnIzcnc5Cg0vZy8xMWozNDQ4OHE4Cg0vZy8xMXNzd3BzZnAzCg0vZy8xMWYzam15M2puCg0vZy8xMWhmNHJfcThyCg0vZy8xMW4xNTB6aHNoCg0vZy8xMWM2N3dtOHRmCg0vZy8xMWRkeGJ6cmNsCg0vZy8xMWg0X2xzMHc0Cg0vZy8xMWoyZnA0bWIyCg0vZy8xMXY1eDM0OGpzEgQSAggBEgQKAggBmgEGCgIXGRAA&src=2&serdesk=1&sa=X&ved=2ahUKEwiurZS73OSEAxX91TgGHYHWCWYQjGp6BAgiEAE&scp=ChVnY2lkOm1hcmtldGluZ19hZ2VuY3kSVxISCRcp3KaMReA7EXyOXMDrZ7gEGhIJYxUdQVlO4DsRQrA4CSlYRf4iFVN1cmF0LCBHdWphcmF0IDM5NTAwNioUDfIgoAwVUZVqKx3Upq4MJZ0nfiswARoYZGlnaXRhbCBtYXJrZXRpbmcgYWdlbmN5IhhkaWdpdGFsIG1hcmtldGluZyBhZ2VuY3kqEE1hcmtldGluZyBhZ2VuY3k%3D')  

search_input = driver.find_element(By.CSS_SELECTOR,'input[class="MDhB7"]')
search_input.clear()
search_input.send_keys("Appliance repair service", Keys.ENTER)

time.sleep(2)
def scrape_page():
     data = driver.find_elements(By.CSS_SELECTOR, '[class="NwqBmc"]')
     for element in data:
         try:
             driver.execute_script("arguments[0].scrollIntoView();", element)
             name = element.find_element(By.CSS_SELECTOR, '.rgnuSb').text.strip()
             rating = element.find_element(By.CSS_SELECTOR, '.OJbIQb').text.strip()
             addresses = element.find_elements(By.XPATH, './/span[2][contains(@class, "hGz87c")]')
             phones = element.find_elements(By.XPATH, './/span[3][contains(@class, "hGz87c")]')
            
             if name and rating:
                 print("Name:", name)
                 print("Rating:", rating)
                
                 if addresses:
                     for address in addresses:
                         address_text = address.text.strip()
                         if address_text:
                             print("Address:", address_text)
                
                 if phones:
                     for phone in phones:
                         phone_text = phone.text.strip()
                         if phone_text:
                             print("Phone:", phone_text)
                
                 print()  # Print an empty line for better readability
                
         except Exception as e:
             print("Error occurred:", e)


scrape_page()
while True:   
     button = driver.find_elements(By.XPATH, '//button[@aria-label="Next"]')[1]
     button.click()
     time.sleep(2)
     scrape_page()
     break



#driver.execute_script("arguments[0].click();", button)
'''
