from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from flask_sqlalchemy import SQLAlchemy
from selenium.webdriver.chrome.options import Options
from IPython.display import display, Image
# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraped_data.db'
db = SQLAlchemy(app)

# Define SQLAlchemy model for scraped data
class Rating(db.Model):
    __tablename__ = 'scraped_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    rating = db.Column(db.String(10))
    count = db. Column(db.String(1000))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    category = db.Column(db.String(20))
    image = db.Column(db.String(255))

# Function to create the database table
def create_table():
    db.create_all()

# Function to insert data into the database
def insert_data(data):
    for item in data:
        new_rating = Rating( name=item['name'], rating=item['rating'], count=item['count'], address=item['addresses'], phone=item['phones'], category=item['category'], image=item['image'])
        db.session.add(new_rating)
    db.session.commit()

# Function to fetch data from the database
def fetch_data():
    return Rating.query.all()

# Function to scrape Google Local Services
def scrape_google_local_services( category,country,city, search_key):
    # Initialize WebDriver
    driver = webdriver.Chrome()
    # Set Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode

    # Initialize WebDriver with Chrome options
    driver = webdriver.Chrome(options=chrome_options)
    
    # Open Google Local Services page
    driver.get('https://www.google.com/localservices/prolist?g2lbs=AIQllVzWSYspFtzaywPV9jv6ozuwdPjt7hfraOfChGkHnMWRs6jF0EN0JnmLVAxCXczEjUzv4oHOVvTL6BdV-38uYjJ1IChxr0ZEAtiL7qHihksvHmIrYX9YXjZaRJZM3RoWbXTEIRAz&hl=en-IN&gl=in&ssta=1&q=digital%20marketing%20agency&oq=digital%20marketing%20agency&slp=MgA6HENoTUlwNk9mdTl6a2hBTVZCUS1EQXgzU1FBV19SAggCYACSAbgCCg0vZy8xMWg1N2sxNTMxCg0vZy8xMWJ3NjlyemhwCg0vZy8xMXFwbTVoY2YyCg0vZy8xMWprNHZ2NXQ1Cg0vZy8xMXM2MXN3ZDg3Cg0vZy8xMXZqaG1tbGZtCg0vZy8xMWZzdm01XzF5Cg0vZy8xMWxjZnE0eV9yCg0vZy8xMWtqajcycnQzCg0vZy8xMXJzYnIzcnc5Cg0vZy8xMWozNDQ4OHE4Cg0vZy8xMXNzd3BzZnAzCg0vZy8xMWYzam15M2puCg0vZy8xMWhmNHJfcThyCg0vZy8xMW4xNTB6aHNoCg0vZy8xMWM2N3dtOHRmCg0vZy8xMWRkeGJ6cmNsCg0vZy8xMWg0X2xzMHc0Cg0vZy8xMWoyZnA0bWIyCg0vZy8xMXY1eDM0OGpzEgQSAggBEgQKAggBmgEGCgIXGRAA&src=2&serdesk=1&sa=X&ved=2ahUKEwiurZS73OSEAxX91TgGHYHWCWYQjGp6BAgiEAE&scp=ChVnY2lkOm1hcmtldGluZ19hZ2VuY3kSVxISCRcp3KaMReA7EXyOXMDrZ7gEGhIJYxUdQVlO4DsRQrA4CSlYRf4iFVN1cmF0LCBHdWphcmF0IDM5NTAwNioUDfIgoAwVUZVqKx3Upq4MJZ0nfiswARoYZGlnaXRhbCBtYXJrZXRpbmcgYWdlbmN5IhhkaWdpdGFsIG1hcmtldGluZyBhZ2VuY3kqEE1hcmtldGluZyBhZ2VuY3k%3D')  
    
    # Find the search input element and input the search query
    search_input = driver.find_element(By.XPATH, '//*[@id="qjZKOb"]')
    search_input.clear()  # Clear any existing text in the search input
    search_input.send_keys(search_key, Keys.ENTER)

    time.sleep(2)  # Wait for the results to load
    data = []
    
    def scrape_page():
        nonlocal data 
        #elements = driver.find_elements(By.CSS_SELECTOR, '[class="NwqBmc"]')
        elements= driver.find_elements(By.CLASS_NAME, 'DVBRsc')
        for element in elements:
            item = {}
            try:
                driver.execute_script("arguments[0].scrollIntoView();", element)
                item['name'] = element.find_element(By.CSS_SELECTOR, '.rgnuSb').text.strip()
                item['rating'] = element.find_element(By.CSS_SELECTOR, '.OJbIQb').text
                item['count'] = element.find_element(By.CLASS_NAME,'leIgTe').text
                item['addresses'] = element.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[1]/div[1]/div/div/div/div[2]/div[3]/span[2]/span').text.strip()
                item['phones'] = element.find_element(By.XPATH, './/span[3][contains(@class, "hGz87c")]').text
                item['category'] = element.find_element(By.XPATH, './/span[contains(@class, "hGz87c")]').text.strip()
                item['image'] = element.find_element(By.CLASS_NAME, 'Fy57pd').get_attribute("src")
                display(Image(url='image'))
                data.append(item)
            except Exception as e:
                print("Error occurred:", e)

    scrape_page()
    while True:   
        try:
            button = driver.find_elements(By.XPATH, '//button[@aria-label="Next"]')[1]
            button.click()
            time.sleep(2)
            scrape_page()
        except:
            break

    # Insert scraped data into the database
    insert_data(data)
    driver.quit()
    return data

# @app.route('/home', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         category = request.form['category']
#         country = request.form['country']
#         city = request.form['city']

#         # Check if data exists in the database
#         ratings = fetch_data()
#         if not ratings:
#             # If data doesn't exist, scrape and store it
#             search_key = category + " " + country + " " + city
#             results = scrape_google_local_services(category, country, city, search_key)
#             ratings = fetch_data()
        
#         return render_template('home.html', ratings=ratings)
#     else:
#         # Fetch all ratings from the database
#         ratings = fetch_data()              
#         return render_template('home.html', ratings=ratings)
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        category = request.form['category']
        country = request.form['country']
        city = request.form['city']

        # Fetch data based on form inputs
        ratings = Rating.query.filter_by(category=category, country=country, city=city).all()

        return render_template('home.html', ratings=ratings)
    else:
        # Fetch all ratings from the database
        ratings = fetch_data()
        return render_template('home.html', ratings=ratings)


from flask import jsonify
@app.route('/scrape', methods=['POST'])
def scrape():
    if request.method == 'POST':
        search_key = request.form['search_key']
        category, country, city = search_key.split()
        
        # Scrape and store data
        scraped_data = scrape_google_local_services(category, country, city, search_key)
    
        
        # Return the scraped data as JSON
        return jsonify(scraped_data), 200
    else:
        return jsonify({'error': 'Invalid request method.'}), 405



@app.route('/')
def index():
     return render_template('index.html')


# @app.route("/scraped", methods=['POST'])
# def scraped():
#     if request.method == "POST":
#         city = request.form['city']
#         search_key = request.form['search_key']
#         search_key += " " + city  # Concatenate city name to the search key
#         results = scrape_google_local_services(city, search_key)
#         return render_template('scraped_data.html', results=results)

if __name__ == '__main__':
    with app.app_context():
        create_table()  # Create the table when the script is run
        app.run(debug=True)









