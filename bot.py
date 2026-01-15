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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Flask Server for Render ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot is alive and burying the evidence!", 200

# --- Configuration ---
TARGET_URL = "https://www.getlinks.info/love/c/pvcapru"
INPUT_1_ID = "yourname"
INPUT_2_ID = "crushname"
ITERATIONS = int(os.getenv("ITERATIONS", "150")) 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger()

class_names = [
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
    logger.info("[SYSTEM] Booting Headless Chrome...")
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
            time.sleep(0.8) # Wait for animation
            parent = dropdowns[idx].find_element(By.XPATH, "./..")
            opts = parent.find_elements(By.CSS_SELECTOR, ".dropdown-menu li")
            if opts:
                choice = random.choice(opts)
                logger.info(f"   [GENDER] Picking {choice.text} for {label}")
                choice.click()
    except Exception as e:
        logger.warning(f"   [!] Gender selection skipped for {label}")

def pollution_worker():
    logger.info("==========================================")
    logger.info("   MISSION: OPERATION CLASSROOM COVERUP   ")
    logger.info("==========================================")
    
    driver = get_driver()
    wait = WebDriverWait(driver, 20) # Smart Wait up to 20 seconds
    
    for i in range(1, ITERATIONS + 1):
        try:
            logger.info(f"\n>>> PROCESSING COMBINATION #{i}...")
            
            # 1. Load Site
            driver.get(TARGET_URL)
            
            # 2. Hard Sleep as requested (Ensure page is fully ready)
            logger.info(f"   [STEP] Loading page... waiting 6s buffer...")
            time.sleep(6) 
            
            # 3. Clear Cookies for a Fresh Identity
            driver.delete_all_cookies()

            # 4. Wait for the name input to exist before typing
            logger.info("   [STEP] Locating name fields...")
            box1 = wait.until(EC.presence_of_element_located((By.ID, INPUT_1_ID)))
            box2 = wait.until(EC.presence_of_element_located((By.ID, INPUT_2_ID)))

            # 5. Pick Names
            n1 = random.choice(class_names)
            n2 = random.choice(class_names)
            while n1 == n2: n2 = random.choice(class_names)
            
            logger.info(f"   [DATA] Pairing: {n1} + {n2}")

            # 6. Enter Data
            box1.send_keys(n1)
            select_gender(driver, 0, "User")
            
            box2.send_keys(n2)
            select_gender(driver, 1, "Crush")

            # 7. Submit
            logger.info("   [STEP] Submitting...")
            box2.send_keys(Keys.RETURN)
            
            logger.info(f"SUCCESS: Posted entry #{i}")
            
            # Delay before next fresh visit
            time.sleep(random.uniform(5, 10))

        except Exception as e:
            logger.error(f"FATAL ERROR on iteration {i}: {e}")
            time.sleep(10) # Wait and retry
            
    driver.quit()
    logger.info("MISSION COMPLETE.")

if __name__ == "__main__":
    threading.Thread(target=pollution_worker, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
