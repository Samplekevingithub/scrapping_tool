from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraped_data.db'
db = SQLAlchemy(app)

class Rating(db.Model):
    __tablename__ = 'scraped_data'  # Match the table name with the existing one
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    rating = db.Column(db.String(10))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))

def create_table():
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scraped_data
                 (id INTEGER PRIMARY KEY, name TEXT, rating TEXT, address TEXT, phone TEXT)''')
    conn.commit()
    conn.close()

 # Function to insert data into SQLite database
def insert_data(data):
     conn = sqlite3.connect('scraped_data.db')
     c = conn.cursor()
     for item in data:
         c.execute("INSERT INTO scraped_data VALUES (?, ?, ?, ?)", (item['name'], item['rating'], item['addresses'], item['phones']))
     conn.commit()
     conn.close()
  
# def insert_data(data):
#     for item in data:
#         new_rating = Rating(name=item['name'], rating=item['rating'], address=item['addresses'], phone=item['phones'])
#         db.session.add(new_rating)
#     db.session.commit()


def fetch_data():
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM scraped_data")
    data = c.fetchall()
    conn.close()
    return data

# Function to scrape Google Local Services
def scrape_google_local_services(city, search_key, scrape_page):
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
                item['addresses'] = element.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[1]/div[1]/div/div/div/div[2]/div[3]/span[2]/span').text.strip()
                item['phones'] = element.find_element(By.XPATH, './/span[3][contains(@class, "hGz87c")]').text
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

    # Instead of appending data to a list, insert it into the database
    insert_data(data)
    for item in data:
         new_rating = Rating(name=item['name'], rating=item['rating'], address=item['addresses'], phone=item['phones'])
         db.session.add(new_rating)
         db.session.commit()

    driver.quit()
    return data
# @app.route('/home')
# def home():
            
       
#         for rating in ratings:
#                 new_rating = Rating(name=rating['name'], rate=rating['rating'],address=rating['address'],phone=rating['phone'])
#                 db.session.add(new_rating)
#         db.session.commit()
#         ratings=Rating.query.all()
#         current_min_rating = 0
#         current_max_rating = 5
        
#         return render_template('home.html' ,ratings=ratings, current_min_rating=current_min_rating, current_max_rating=current_max_rating)

@app.route('/home')
def home():
    # Fetch all ratings from the database
    ratings = Rating.query.all()
    
    # Define default filter values
    current_min_rating = 0
    current_max_rating = 5
    
    # Render the home template with ratings and filter values
    return render_template('home.html', ratings=ratings, current_min_rating=current_min_rating, current_max_rating=current_max_rating)

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
        #results = scrape_google_local_services(city, search_key, scrape_page)
        scrape_google_local_services(city, search_key, scrape_page)
        results = fetch_data()
        return render_template('scraped_data.html', results=results)



if __name__ == '__main__':
    #create_table()  # Create the table when the script is run
    app.run(debug=True)




'''from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from flask_sqlalchemy import SQLAlchemy
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
    address = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    category = db.Column(db.String(20))

# Function to create the database table
def create_table():
    db.create_all()

# Function to insert data into the database
def insert_data(data):
    for item in data:
        new_rating = Rating(name=item['name'], rating=item['rating'], address=item['addresses'], phone=item['phones'], category=item['category'])
        db.session.add(new_rating)
    db.session.commit()

# Function to fetch data from the database
def fetch_data():
    return Rating.query.all()

# Function to scrape Google Local Services
def scrape_google_local_services(city, search_key):
    # Initialize WebDriver
    driver = webdriver.Chrome()
    
    # Open Google Local Services page
    driver.get('https://www.google.com/localservices/prolist?g2lbs=AIQllVzWSYspFtzaywPV9jv6ozuwdPjt7hfraOfChGkHnMWRs6jF0EN0JnmLVAxCXczEjUzv4oHOVvTL6BdV-38uYjJ1IChxr0ZEAtiL7qHihksvHmIrYX9YXjZaRJZM3RoWbXTEIRAz&hl=en-IN&gl=in&ssta=1&q=digital%20marketing%20agency&oq=digital%20marketing%20agency&slp=MgA6HENoTUlwNk9mdTl6a2hBTVZCUS1EQXgzU1FBV19SAggCYACSAbgCCg0vZy8xMWg1N2sxNTMxCg0vZy8xMWJ3NjlyemhwCg0vZy8xMXFwbTVoY2YyCg0vZy8xMWprNHZ2NXQ1Cg0vZy8xMXM2MXN3ZDg3Cg0vZy8xMXZqaG1tbGZtCg0vZy8xMWZzdm01XzF5Cg0vZy8xMWxjZnE0eV9yCg0vZy8xMWtqajcycnQzCg0vZy8xMXJzYnIzcnc5Cg0vZy8xMWozNDQ4OHE4Cg0vZy8xMXNzd3BzZnAzCg0vZy8xMWYzam15M2puCg0vZy8xMWhmNHJfcThyCg0vZy8xMW4xNTB6aHNoCg0vZy8xMWM2N3dtOHRmCg0vZy8xMWRkeGJ6cmNsCg0vZy8xMWg0X2xzMHc0Cg0vZy8xMWoyZnA0bWIyCg0vZy8xMXY1eDM0OGpzEgQSAggBEgQKAggBmgEGCgIXGRAA&src=2&serdesk=1&sa=X&ved=2ahUKEwiurZS73OSEAxX91TgGHYHWCWYQjGp6BAgiEAE&scp=ChVnY2lkOm1hcmtldGluZ19hZ2VuY3kSVxISCRcp3KaMReA7EXyOXMDrZ7gEGhIJYxUdQVlO4DsRQrA4CSlYRf4iFVN1cmF0LCBHdWphcmF0IDM5NTAwNioUDfIgoAwVUZVqKx3Upq4MJZ0nfiswARoYZGlnaXRhbCBtYXJrZXRpbmcgYWdlbmN5IhhkaWdpdGFsIG1hcmtldGluZyBhZ2VuY3kqEE1hcmtldGluZyBhZ2VuY3k%3D')  
    
    # Find the search input element and input the search query
    #search_input = driver.find_element(By.CSS_SELECTOR, 'input[class="MDhB7"]')
    search_input = driver.find_element(By.XPATH, '//*[@id="qjZKOb"]')
    search_input.clear()  # Clear any existing text in the search input
    search_input.send_keys(search_key, Keys.ENTER)

    time.sleep(2)  # Wait for the results to load
    data = []
    
    def scrape_page():
        nonlocal data 
        elements = driver.find_elements(By.CSS_SELECTOR, '[class="NwqBmc"]')
        for element in elements:
            item = {}
            try:
                driver.execute_script("arguments[0].scrollIntoView();", element)
                item['name'] = element.find_element(By.CSS_SELECTOR, '.rgnuSb').text.strip()
                item['rating'] = element.find_element(By.CSS_SELECTOR, '.OJbIQb').text
                item['addresses'] = element.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[1]/div[1]/div/div/div/div[2]/div[3]/span[2]/span').text.strip()
                item['phones'] = element.find_element(By.XPATH, './/span[3][contains(@class, "hGz87c")]').text
                #item['category'] =element.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[1]/div[3]/div[3]/c-wiz/div/div/div[1]/c-wiz/div/div[1]/div[1]/div/div/div/div[2]/div[2]/span').text.strip()
                item['category'] = element.find_element(By.XPATH, './/span[contains(@class, "hGz87c")]').text.strip()

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


@app.route('/home')
def home():
    # Fetch selected category from the form
    selected_category = request.args.get('category')
    
    # Fetch all ratings from the database
    ratings = fetch_data()
    
    # Filter ratings based on the selected category
    if selected_category and selected_category != '0':
        ratings = [rating for rating in ratings if rating.category.lower() == selected_category.lower()]
    
    # Define default filter values
    current_min_rating = 0
    current_max_rating = 5
    
    # Render the home template with filtered ratings and filter values
    return render_template('home.html', ratings=ratings, current_min_rating=current_min_rating, current_max_rating=current_max_rating)




@app.route('/')
def index():
     return render_template('index.html')

@app.route("/scraped", methods=['POST'])
def scraped():
    if request.method == "POST":
        city = request.form['city']
        search_key = request.form['search_key']
        search_key += " " + city  # Concatenate city name to the search key
        results=scrape_google_local_services(city, search_key)
        #results = fetch_data()
        return render_template('scraped_data.html', results=results)

if __name__ == '__main__':
    with app.app_context():
        create_table()  # Create the table when the script is run
        app.run(debug=True)
'''

'''<form class="form-container" action="/home" method="post">

        <div class="form-container">
            <b><label for="category">Category:</label></b>
            <select id="category" name="category">
                <option value="0">--------------------------------------------------------------------------------Please choose a category------------------------------------------------------------------------------------------------------</option>
                <option value="Software">Software</option>
                <option value="Agency">Agency</option>
                <option value="Service">Service</option>
                <option value="Hospital">Hospital</option>
                <option value="Restaurant">Restaurant </option>
                <option value="Bank">Bank </option>
                <option value="Club">Club</option>
	 </select><br><br>

            <b> <label for="rating">Rating:</label></b>
            <div id="rating-container" class="rating-container">
              <b> <span class="rating" data-value="1">★</span>
                <span class="rating" data-value="2">★</span>
                <span class="rating" data-value="3">★</span>
                <span class="rating" data-value="4">★</span>
                <span class="rating" data-value="5">★</span></b> 
            </div><br><br>
            <input type="hidden" id="hidden-category" name="hidden-category">
            <input type="hidden" id="hidden-rating" name="hidden-rating">
            <div class="country-city-container">
                <div class="form-group">
                  <b><label for="country">Country:</label></b>
                    <select id="country" name="country" onchange="populateCities()">
                        <option value="0">----------------------------Please choose a country--------------------------------</option>
                        <option value="Afghanistan">Afghanistan</option>
                        <option value="Åland Islands">Åland Islands</option>
                        <option value="Albania">Albania</option>
                        <option value="Algeria">Algeria</option>
                        <option value="American Samoa">American Samoa</option>
	 </select>
                </div>

                <div class="form-group">
                   <b> <label for="city">City:</label></b>
                    <select id="city" name="city">
                        <option value="0">------------------------------Please choose a city----------------------------------</option>
                        <option value="Kabul">Kabul</option>
                        <option value="Mariehamn">Mariehamn</option>
                        <option value="Tirana">Tirana</option>
                        <option value="Algiers">Algeria</option>
                        <option value="Pago Pago">Pago</option>
                        <option value="Andorra la Vella">Andorra la Vella</option>
                        <option value="Luanda">Luanda</option>
                        <option value="The Valley">The Valley</option>
	  </select>
                </div>
            </div>
        </div>


        <script>
            var citiesByCountry = {
                "Afghanistan": ["Kabul", "Kandahar"],
                "Åland Islands": ["Mariehamn", "Jomala"],
                "Albania": ["Tirana", "Durres"],
                "Algeria": ["Algiers", "Oran"],
                "American Samoa": ["Pago Pago", "Fagatogo"],
                "Andorra": ["Andorra la Vella", "Escaldes-Engordany"],
	    };

            function populateCities() {
                var countrySelect = document.getElementById("country");
                var citySelect = document.getElementById("city");
                var country = countrySelect.value;

                // Clear existing options
                citySelect.innerHTML = '';

                // Populate cities based on selected country
                if (country in citiesByCountry) {
                    var cities = citiesByCountry[country];
                    for (var i = 0; i < cities.length; i++) {
                        addOption(citySelect, cities[i], cities[i]);
                    }
                } else {
                    addOption(citySelect, "--Please choose a city--", "0");
                }
            }

            function addOption(selectElement, text, value) {
                var option = document.createElement("option");
                option.text = text;
                option.value = value;
                selectElement.add(option);
            }
        </script>

        <table id="ratings-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Rate</th>
                    <th>Address</th>
                    <th>Phone</th>
                    <th>Category</th>
                </tr>
            </thead>
            <tbody>
            <tbody>
                {% for rating in ratings %}
                <tr data-rate="{{ rating.rating }}">
                    <td>{{ rating.name }}</td>
                    <td>{{ rating.rating }}</td>
                    <td>{{ rating.address }}</td>
                    <td>{{ rating.phone }}</td>
                    <td>{{ rating.category }}</td>
                </tr>
                {% endfor %}
            </tbody>


            </tbody>
        </table>
        <div class="submit-button-container">
            <input type="submit" value="Submit">
        </div>


        <!--this is a rating jquery-->
       <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

        <script>
            $(document).ready(function () {
                var current_min_rating = 0;
                var current_max_rating = 5;

                // Function to filter the ratings table
                function filterRatings() {
                    var selectedCategory = $('#category').val(); // Get the selected category
                    var selectedCity = $('#city').val(); // Get the selected city
                    var selectedCountry = $('#country').val(); // Get the selected country
                    $('#category').change(function() {
                        filterRatings();
                    });

                    // Event listener for city selection
                    $('#city').change(function() {
                        filterRatings();
                    });

                    // Event listener for country selection
                    $('#country').change(function() {
                        filterRatings();
                    });
                    console.log("Selected City:", selectedCity);
                    console.log("Selected Country:", selectedCountry);
                    console.log("Selected Category:", selectedCategory);
                    $('#ratings-table tbody tr').hide();
                    $('#ratings-table tbody tr[data-rate]').each(function () {
                        var data_rate = parseInt($(this).data('rate'));
                        var category = $(this).find('td:eq(4)').text();
                        var address = $(this).find('td:eq(2)').text();
                        console.log("Address:", address);
                        console.log("Category:", category);
                        
                        // Check if category, city, state, and rating match the selected values
                        if ((selectedCategory === "0" || category.toLowerCase().includes(selectedCategory.toLowerCase())) &&
                            (selectedCity === "0" || address.toLowerCase().includes(selectedCity.toLowerCase())) &&
                            (selectedCountry === "0" || address.toLowerCase().includes(selectedCountry.toLowerCase())) &&
                            (data_rate >= current_min_rating && data_rate <= current_max_rating)) {
                            $(this).show();
                        }
                    });
                }
       
                // Event listener for rating selection
                $('.rating').click(function () {
                    $('.rating.selected').removeClass('selected');
                    $(this).addClass('selected');
                    current_min_rating = parseInt($(this).data('value'));
                    current_max_rating = current_min_rating;
                    filterRatings();
                    // $('#ratings-table').show();
                });
 
                // Event listener for form submission
                $('input[type="submit"]').click(function (e) {
                    e.preventDefault();
                    // Show the ratings table if ratings were filtered
                    if (current_min_rating > 0) {
                        filterRatings();
                        $('#ratings-table').show();
                    }
                });
            });
        </script>
            

        <script src="{{url_for('static',filename='js/script.js')}}">
        </script>
    </form>
</body>

</html>'''