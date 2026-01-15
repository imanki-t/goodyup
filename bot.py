import os
import time
import random
import logging
import sys
import threading
import io
from flask import Flask, send_file, render_template_string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# --- Flask Setup ---
app = Flask(__name__)

# Global variable to store the latest screenshot
last_screenshot = None
status_msg = "Initializing..."
current_pairing = "None"

@app.route('/')
def monitor():
    # Simple HTML dashboard to view the bot's progress
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bot Live Monitor</title>
        <meta http-equiv="refresh" content="5">
        <style>
            body { font-family: sans-serif; background: #121212; color: white; text-align: center; padding: 20px; }
            .container { max-width: 800px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 15px; border: 1px solid #333; }
            img { width: 100%; border-radius: 10px; border: 2px solid #f5576c; margin-top: 20px; }
            .status { font-size: 1.2em; color: #f093fb; font-weight: bold; }
            .info { color: #aaa; margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Class IX B Pollution Bot</h1>
            <p class="status">Status: {{ status }}</p>
            <p class="info">Current Pair: {{ pair }}</p>
            <p class="info"><i>Page auto-refreshes every 5 seconds</i></p>
            {% if has_img %}
                <img src="/screenshot.png" alt="Live View">
            {% else %}
                <p>Waiting for first screenshot...</p>
            {% endif %}
        </div>
    </body>
    </html>
    """
    return render_template_string(html, status=status_msg, pair=current_pairing, has_img=(last_screenshot is not None))

@app.route('/screenshot.png')
def serve_screenshot():
    if last_screenshot:
        return send_file(io.BytesIO(last_screenshot), mimetype='image/png')
    return "No screenshot yet", 404

# --- Bot Logic ---
TARGET_URL = "https://www.getlinks.info/love/c/pvcapru"
ITERATIONS = int(os.getenv("ITERATIONS", "1035"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(message)s', handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger()

class_names = ["Aarav Agarwal", "Aarus Kumar", "Aarvi Shailya Patel", "Abhijeet Oraon", "Adrija Chatterjee", "Adwitiya Ashok", "Akshita Tripti", "Ananya Sejal", "Ananya Sinha", "Ankit Kumar", "Annanya Srivastava", "Anushka Choudhary", "Anushka Kedia", "Arnav Gupta", "Arnav Jairaj", "Arnav Shekhar", "Atifa Shakeel", "Avyuday Bhagat", "Ayush Kumar", "Bhavna Kumari", "Bhavya Mishra", "Chinmay Sharma", "Darshita Vini", "Jahnvi Shree Gaurav", "Jaya Shambhavi", "Jayesh Kumar", "Kushagra Bhardwaj", "Lakshya Vishal Bhagat", "Mayank Sahu", "Prachi Singh", "Prakhar", "Priyank Oraon", "Reevika", "Riddhi Rani", "Rudra Pratap Jha", "Sarthak Raj", "Shashwat Sinha", "Shreya Om", "Shreya Raj", "Shreyash Ayush", "Shreyashi Jaiswal", "Shuryansh", "Soumya Sinha", "Swarit Oraon", "Tanmay Maheshwari", "Vaibhav Raj"]

def take_capture(driver):
    global last_screenshot
    try:
        last_screenshot = driver.get_screenshot_as_png()
    except:
        pass

def select_gender(driver, idx, label):
    try:
        dropdowns = driver.find_elements(By.CSS_SELECTOR, ".dropdown .select")
        if len(dropdowns) > idx:
            dropdowns[idx].click()
            time.sleep(0.5)
            parent = dropdowns[idx].find_element(By.XPATH, "./..")
            opts = parent.find_elements(By.CSS_SELECTOR, ".dropdown-menu li")
            if opts:
                random.choice(opts).click()
                return True
    except: pass
    return False

def pollution_worker():
    global status_msg, current_pairing
    logger.info("Bot Worker Started.")
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,1024") # Set size for screenshot
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    for i in range(1, ITERATIONS + 1):
        try:
            status_msg = f"Navigating to site (Entry {i}/{ITERATIONS})"
            driver.get(TARGET_URL)
            time.sleep(3)
            driver.delete_all_cookies()
            take_capture(driver)

            n1, n2 = random.sample(class_names, 2)
            current_pairing = f"{n1} + {n2}"
            status_msg = "Entering Names & Genders"

            driver.find_element(By.ID, "yourname").send_keys(n1)
            select_gender(driver, 0, "User")
            driver.find_element(By.ID, "crushname").send_keys(n2)
            select_gender(driver, 1, "Crush")
            
            take_capture(driver) # See the form filled out
            
            status_msg = "Submitting Form..."
            driver.find_element(By.ID, "crushname").send_keys(Keys.RETURN)
            
            time.sleep(3)
            take_capture(driver) # See the result page
            logger.info(f"Iteration {i} Success: {current_pairing}")
            
            status_msg = "Success! Resting..."
            time.sleep(random.uniform(5, 10))

        except Exception as e:
            status_msg = f"Error: {str(e)}"
            time.sleep(10)
            
    driver.quit()
    status_msg = "Mission Complete!"

if __name__ == "__main__":
    threading.Thread(target=pollution_worker, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
