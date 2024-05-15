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
    location = db.Column(db.String(255))  # Add location field
    image = db.Column(db.String(255))
    

# Function to create the database table
def create_table():
    db.create_all()

# Function to insert data into the database
def insert_data(data):
    for item in data:
        new_rating = Rating( name=item['name'], rating=item['rating'], count=item['count'], address=item['addresses'], phone=item['phones'], category=item['category'], location=item['location'],image=item['image'])
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
                display(Image(url=item['image']))
                item['location'] = element.find_element(By.XPATH, './/a[@aria-label="Directions"]').get_attribute("href")(url=item['location'])
                

                data.append(item)
            except Exception as e:
                print("Error occurred:", e)
#
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


if __name__ == '__main__':
    with app.app_context():
        create_table()  # Create the table when the script is run
        app.run(debug=True)
'''
from fastapi import FastAPI
import graphene
from pydantic import BaseModel
from sqlalchemy import create_engine,Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphene import ObjectType, Field, String, ID, Int
from starlette.graphql import GraphQLApp
app=FastAPI()
SQLALCHEMY_DATABASE_URL = "sqlite:///./books.db"
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    published_date = Column(Date)
    isbn = Column(String, index=True)
    num_pages = Column(Integer)
    cover_image_url = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)

class BookModel(BaseModel):
    title: str
    author: str
    published_date: str
    isbn: str
    num_pages: int
    cover_image_url: str = None

class BookType(SQLAlchemyObjectType):
    class Meta:
        model = Book
        interfaces = (graphene.relay.Node,)

class Query(ObjectType):
    books=graphene.List(BookType)
    Book=graphene.Field(BookType,id=graphene.Int())

    def resolve_books(self, info):
        return SessionLocal().query(Book).all()
    def resolve_books(self, info, id):
        return SessionLocal().query(Book).filter(Book.id==id).first()
    
Schema = graphene.Schema(query=Query)
app.add_route("/graphql", GraphQLApp(schema=Schema(query=Query)))



INFO:     Will watch for changes in these directories: ['D:\\Book Management System']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12272] using WatchFiles
Process SpawnProcess-1:
Traceback (most recent call last):
  File "C:\Program Files\Python311\Lib\multiprocessing\process.py", line 314, in _bootstrap
    self.run()
  File "C:\Program Files\Python311\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
  File "D:\Book Management System\venv\Lib\site-packages\uvicorn\_subprocess.py", line 78, in subprocess_started
    target(sockets=sockets)
  File "D:\Book Management System\venv\Lib\site-packages\uvicorn\server.py", line 65, in run
    return asyncio.run(self.serve(sockets=sockets))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\asyncio\runners.py", line 190, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\asyncio\base_events.py", line 653, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "D:\Book Management System\venv\Lib\site-packages\uvicorn\server.py", line 69, in serve
    await self._serve(sockets)
  File "D:\Book Management System\venv\Lib\site-packages\uvicorn\server.py", line 76, in _serve
    config.load()
  File "D:\Book Management System\venv\Lib\site-packages\uvicorn\config.py", line 433, in load
    self.loaded_app = import_from_string(self.app)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "D:\Book Management System\venv\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Program Files\Python311\Lib\importlib\__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1204, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1176, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1147, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 690, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 940, in exec_module
  File "<frozen importlib._bootstrap>", line 241, in _call_with_frames_removed
  File "D:\Book Management System\app.py", line 2, in <module>
    import graphene
  File "D:\Book Management System\venv\Lib\site-packages\graphene\__init__.py", line 3, in <module>
    from .types import (
  File "D:\Book Management System\venv\Lib\site-packages\graphene\types\__init__.py", line 2, in <module>
    from graphql import ResolveInfo
ImportError: cannot import name 'ResolveInfo' from 'graphql' (D:\Book Management System\venv\Lib\site-packages\graphql\__init__.py)

'''