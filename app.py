from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

def scrape_google_local_services(search_key):
    driver = webdriver.Chrome()

    # Open the Google Local Services page
    driver.get('https://www.google.com/localservices/prolist?g2lbs=AIQllVzWSYspFtzaywPV9jv6ozuwdPjt7hfraOfChGkHnMWRs6jF0EN0JnmLVAxCXczEjUzv4oHOVvTL6BdV-38uYjJ1IChxr0ZEAtiL7qHihksvHmIrYX9YXjZaRJZM3RoWbXTEIRAz&hl=en-IN&gl=in&ssta=1&q=digital%20marketing%20agency&oq=digital%20marketing%20agency&slp=MgA6HENoTUlwNk9mdTl6a2hBTVZCUS1EQXgzU1FBV19SAggCYACSAbgCCg0vZy8xMWg1N2sxNTMxCg0vZy8xMWJ3NjlyemhwCg0vZy8xMXFwbTVoY2YyCg0vZy8xMWprNHZ2NXQ1Cg0vZy8xMXM2MXN3ZDg3Cg0vZy8xMXZqaG1tbGZtCg0vZy8xMWZzdm01XzF5Cg0vZy8xMWxjZnE0eV9yCg0vZy8xMWtqajcycnQzCg0vZy8xMXJzYnIzcnc5Cg0vZy8xMWozNDQ4OHE4Cg0vZy8xMXNzd3BzZnAzCg0vZy8xMWYzam15M2puCg0vZy8xMWhmNHJfcThyCg0vZy8xMW4xNTB6aHNoCg0vZy8xMWM2N3dtOHRmCg0vZy8xMWRkeGJ6cmNsCg0vZy8xMWg0X2xzMHc0Cg0vZy8xMWoyZnA0bWIyCg0vZy8xMXY1eDM0OGpzEgQSAggBEgQKAggBmgEGCgIXGRAA&src=2&serdesk=1&sa=X&ved=2ahUKEwiurZS73OSEAxX91TgGHYHWCWYQjGp6BAgiEAE&scp=ChVnY2lkOm1hcmtldGluZ19hZ2VuY3kSVxISCRcp3KaMReA7EXyOXMDrZ7gEGhIJYxUdQVlO4DsRQrA4CSlYRf4iFVN1cmF0LCBHdWphcmF0IDM5NTAwNioUDfIgoAwVUZVqKx3Upq4MJZ0nfiswARoYZGlnaXRhbCBtYXJrZXRpbmcgYWdlbmN5IhhkaWdpdGFsIG1hcmtldGluZyBhZ2VuY3kqEE1hcmtldGluZyBhZ2VuY3k%3D')  

    # Find the search input element and input the search query
    search_input = driver.find_element(By.CSS_SELECTOR, 'input[class="MDhB7"]')
    search_input.clear()  # Clear any existing text in the search input
    search_input.send_keys(search_key, Keys.ENTER)

    time.sleep(2)  # Wait for the results to load

    # Collect data
    data = []
    elements = driver.find_elements(By.CSS_SELECTOR, '[class="NwqBmc"]')
    for element in elements:
        item = {}
        try:
            item['name'] = element.find_element(By.CSS_SELECTOR, '.rgnuSb').text
            item['rating'] = element.find_element(By.CSS_SELECTOR, '.OJbIQb').text
            item['addresses'] = element.find_element(By.XPATH, './/span[2][contains(@class, "hGz87c")]').text
            item['phones'] = element.find_element(By.XPATH, './/span[3][contains(@class, "hGz87c")]').text

            data.append(item)
        except Exception as e:
            print("Error occurred:", e)

    driver.quit()  # Quit the driver after scraping
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/scraped", methods=['POST'])
def scraped():
    if request.method == "POST":
        search_key = request.form['search_key']
        results = scrape_google_local_services(search_key)
        return render_template('scraped_data.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
