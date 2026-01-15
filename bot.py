import os
import time
import random
import logging
import sys
import threading
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# --- Flask Server for Render Health Check ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is running and polluting!", 200

# --- Configuration ---
TARGET_URL = os.getenv("TARGET_URL", "https://www.getlinks.info/love/c/pvcapru")
INPUT_1_ID = "yourname"
INPUT_2_ID = "crushname"
ITERATIONS = int(os.getenv("ITERATIONS", "150")) 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger()

real_class_names = [
    "Aarav Agarwal", "Aarus Kumar", "Aarvi Shailya Patel", "Abhijeet Oraon",
    "Adrija Chatterjee", "Adwitiya Ashok", "Akshita Tripti", "Ananya Sejal",
    "Ananya Sinha", "Ankit Kumar", "Annanya Srivastava", "Anushka Choudhary",
    "Anushka Kedia", "Arnav Gupta", "Arnav Jairaj", "Arnav Shekhar",
    "Atifa Shakeel", "Avyuday Bhagat", "Ayush Kumar", "Bhavna Kumari",
    "Bhavya Mishra", "Chinmay Sharma", "Darshita Vini", "Jahnvi Shree Gaurav",
    "Jaya Shambhavi", "Jayesh Kumar", "Kushagra Bhardwaj", "Lakshya Vishal Bhagat",
    "Mayank Sahu", "Prachi Singh", "Prakhar", "Priyank Oraon", "Reevika",
    "Riddhi Rani", "Rudra Pratap Jha", "Sarthak Raj", "Shashwat Sinha",
    "Shreya Om", "Shreya Raj", "Shreyash Ayush", "Shreyashi Jaiswal",
    "Shuryansh", "Soumya Sinha", "Swarit Oraon", "Tanmay Maheshwari",
    "Vaibhav Raj"
]

def get_driver():
    logger.info("Initializing Headless Chrome...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def select_gender(driver, idx, label):
    try:
        dropdowns = driver.find_elements(By.CSS_SELECTOR, ".dropdown .select")
        if len(dropdowns) > idx:
            dropdowns[idx].click()
            time.sleep(0.5)
            parent = dropdowns[idx].find_element(By.XPATH, "./..")
            opts = parent.find_elements(By.CSS_SELECTOR, ".dropdown-menu li")
            if opts:
                choice = random.choice(opts)
                val = choice.text
                choice.click()
                logger.info(f"   [Step] Selected Gender for {label}: {val}")
    except:
        logger.warning(f"   [!] Failed to click gender for {label}")

def pollution_worker():
    logger.info("==========================================")
    logger.info("   STARTING DATA POLLUTION MISSION        ")
    logger.info(f"   Target URL: {TARGET_URL}")
    logger.info("==========================================")
    
    driver = get_driver()
    
    for i in range(1, ITERATIONS + 1):
        try:
            logger.info(f">>> STARTING COMBINATION #{i}")
            
            # 1. Access Site
            logger.info(f"   [Step] Navigating to {TARGET_URL}...")
            driver.get(TARGET_URL)
            time.sleep(random.uniform(2, 4))
            driver.delete_all_cookies()

            # 2. Pick Names
            n1 = random.choice(real_class_names)
            n2 = random.choice(real_class_names)
            while n1 == n2: n2 = random.choice(real_class_names)
            
            logger.info(f"   [Data] Pairing: {n1} (User) + {n2} (Crush)")

            # 3. Enter Names & Genders
            driver.find_element(By.ID, INPUT_1_ID).send_keys(n1)
            select_gender(driver, 0, "User")
            
            driver.find_element(By.ID, INPUT_2_ID).send_keys(n2)
            select_gender(driver, 1, "Crush")

            # 4. Submit
            logger.info("   [Step] Submitting Form...")
            driver.find_element(By.ID, INPUT_2_ID).send_keys(Keys.RETURN)
            
            logger.info(f"DONE: Successfully posted {n1} + {n2}")
            time.sleep(random.uniform(3, 8))

        except Exception as e:
            logger.error(f"ERROR on iteration {i}: {e}")
            time.sleep(5)
            
    driver.quit()
    logger.info("==========================================")
    logger.info("   MISSION COMPLETE - SECRET BURIED       ")
    logger.info("==========================================")

if __name__ == "__main__":
    # Start the bot in a background thread
    threading.Thread(target=pollution_worker, daemon=True).start()
    
    # Start the web server for Render (Port 10000)
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
