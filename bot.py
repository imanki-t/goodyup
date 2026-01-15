import os
import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Configuration ---
TARGET_URL = os.getenv("TARGET_URL", "https://www.getlinks.info/love/c/pvcapru")
INPUT_1_ID = "yourname"
INPUT_2_ID = "crushname"
ITERATIONS = int(os.getenv("ITERATIONS", "300")) 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# --- Class List (From your PDF) ---
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
    """Sets up Chrome in headless mode for the Render server."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def select_random_gender(driver, index):
    """
    Handles the custom dropdowns.
    index 0 = The first dropdown (Your Gender)
    index 1 = The second dropdown (Crush Gender)
    """
    try:
        # Find all custom dropdown triggers
        dropdowns = driver.find_elements(By.CSS_SELECTOR, ".dropdown .select")
        
        if len(dropdowns) > index:
            # Click the dropdown to open it
            dropdowns[index].click()
            time.sleep(0.5)
            
            # Find the options (Male/Female) inside this specific dropdown
            # We look for the parent (.dropdown) then find the list items (.dropdown-menu li)
            parent = dropdowns[index].find_element(By.XPATH, "./..")
            options = parent.find_elements(By.CSS_SELECTOR, ".dropdown-menu li")
            
            # Pick a random gender (Male or Female)
            if options:
                random.choice(options).click()
                time.sleep(0.2)
    except Exception as e:
        logger.warning(f"Could not select gender for index {index}: {e}")

def run_bot():
    logger.info(f"Targeting URL: {TARGET_URL}")
    logger.info("Initializing 'Classroom Cover-Up' protocol with GENDERS...")
    driver = get_driver()
    
    try:
        for i in range(ITERATIONS):
            try:
                driver.get(TARGET_URL)
                time.sleep(random.uniform(2, 4))
                driver.delete_all_cookies()
                
                # --- 1. Enter Your Name ---
                n1 = random.choice(real_class_names)
                box1 = driver.find_element(By.ID, INPUT_1_ID)
                box1.clear()
                box1.send_keys(n1)
                time.sleep(random.uniform(0.2, 0.5))
                
                # --- 2. Select Your Gender (First Dropdown) ---
                select_random_gender(driver, 0)
                
                # --- 3. Enter Crush Name ---
                n2 = random.choice(real_class_names)
                while n1 == n2:
                    n2 = random.choice(real_class_names)
                
                box2 = driver.find_element(By.ID, INPUT_2_ID)
                box2.clear()
                box2.send_keys(n2)
                time.sleep(random.uniform(0.2, 0.5))

                # --- 4. Select Crush Gender (Second Dropdown) ---
                select_random_gender(driver, 1)

                # --- 5. Submit ---
                # Sometimes hitting enter on the name box is safer than clicking the button
                box2.send_keys(Keys.RETURN)
                
                logger.info(f"[{i+1}/{ITERATIONS}] Posted: {n1} + {n2}")
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                logger.error(f"Error on iteration {i+1}: {e}")
                time.sleep(5)

    finally:
        driver.quit()
        logger.info("Mission Complete.")

if __name__ == "__main__":
    run_bot()
