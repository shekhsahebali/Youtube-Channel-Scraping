import os
import re
import time
import requests
import unicodedata
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ==========================
# Config
# ==========================
HANDALE = input("Enter the channel handel: ")
if HANDALE == "":
    exit("Handel cannot be empty")
DOWNLOAD_iMAGES_Prompt = input("Do you want to download thumbnails? (y/n) default Yes: ").lower()

if DOWNLOAD_iMAGES_Prompt == "n":
    DOWNLOAD_iMAGES = False
else:
    DOWNLOAD_iMAGES = True

REQUEST_TIMEOUT = 15

URL=f'https://www.youtube.com/@{HANDALE}/videos'
IMG_dir = HANDALE+'_img'
OUTPUT_FILE_NAME= HANDALE+'_data.csv'



# ==========================
# Selenium Setup
# ==========================
options = Options()
options.binary_location = "../chromium/chrome"
# options.add_argument("--disable-gpu")
# options.add_argument("--headless=new")
# options.add_argument("--no-sandbox")
options.add_argument("--start-maximized")

service = Service("../chromiumdriver/chromedriver")
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 10)

# ==========================
# Helpers
# ==========================

def ensure_dir(path: str):
    if not os.path.exists(path):
      os.makedirs(path, exist_ok=True)

def scroll_to_end(driver, pause_time=2, max_attempts=50):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    attempts = 0

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(pause_time)

        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
            attempts += 1
            if attempts >= 3:  
                break
        else:
            attempts = 0
            last_height = new_height
            print(f"Scrolled to {new_height} pixels.")

    print("Reached end of page.")


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = re.sub(r"^-+|-+$", "", text)
    return text


# ==========================
# Main Logic
# ==========================
alldata = []
total_downloaded = 0

driver.get(URL)

if DOWNLOAD_iMAGES:
    ensure_dir(IMG_dir)

if os.path.exists(OUTPUT_FILE_NAME):
    os.remove(OUTPUT_FILE_NAME)

wait.until(
    EC.presence_of_element_located((By.ID, "contents"))
)

print("Scrolling to end of page...")
start_time = time.time()
scroll_to_end(driver)
driver.minimize_window()


videos = driver.find_elements(By.CSS_SELECTOR, "ytd-rich-item-renderer")

print(f"Found {len(videos)} videos\n")

print("Extracting data...\n")

for idx, video in enumerate(videos, start=1):
    try:
        # Title
        title_el = video.find_element(By.ID, "video-title")
        title = title_el.text.strip()

        #URL
        url_el = video.find_element(By.XPATH, ".//ytd-thumbnail/a")
        url = url_el.get_attribute("href")

        # Thumbnail
        img_el = video.find_element(By.CSS_SELECTOR, "img")
        img_url = img_el.get_attribute("src") or img_el.get_attribute("data-src")
        if img_url:
         img_url = img_url.split("?")[0]

       # Views
        try:
            views = video.find_element(
                By.XPATH,
                ".//span[contains(text(),'views')]"
            ).text
        except:
            views = ""

        # Post time
        try:
            post_time = video.find_element(
                By.XPATH,
                ".//span[contains(text(),'ago')]"
            ).text
        except:
            post_time = ""


        if DOWNLOAD_iMAGES:
            # Download thumbnail
            slug = slugify(title)
            img_name = f"{slug}.jpg"
            img_path = os.path.join(IMG_dir, img_name)

            r = requests.get(img_url, timeout=REQUEST_TIMEOUT)
            if r.status_code == 200:
                with open(img_path, "wb") as f:
                    f.write(r.content)
                total_downloaded += 1

        data = {
            "title": title,
            'views': views,
            "post_time": post_time,
            "url": url,
            "thumbnail_url": img_url
            
        }
        if DOWNLOAD_iMAGES:
            data["thumbnail_path"] = img_path

        alldata.append(data)
        print(f"[✓] {idx}. {title}")
        


    except Exception as e:
        print(f"[!] Skipped video {idx}: {e}")


    
pd.DataFrame(alldata).to_csv(OUTPUT_FILE_NAME, index=True)

driver.quit()
end_time = time.time()

elapsed = end_time - start_time
minutes = int(elapsed // 60)
seconds = elapsed % 60

print(f"\nScraping took {minutes}m {seconds:.2f}s to complete {len(videos)} videos.")

