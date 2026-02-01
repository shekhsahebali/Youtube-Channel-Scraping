# Youtube Video Scraper

Youtube Video Scraper is a Python script that scrapes video information from a YouTube channel and saves it to a CSV file.

Perfect for analysts, sellers, and developers looking to automate video data collection.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/).

### Recommended browser
Chromium-based browsers.
- Chromium version:- 145.0.7568.0 
```sh
npx @puppeteer/browsers install chrome@145.0.7568.0
```
- ChromeDriver version:- 145.0.7568.0 
```sh
npx @puppeteer/browsers install chromedriver@145.0.7568.0
```
for more info [https://www.chromium.org/getting-involved/download-chromium/](https://www.chromium.org/getting-involved/download-chromium/)

### Used python Library
```requests
pillow
selenium
unicodedata
pandas
```
## Project Setup
- Clone the repo

```sh
git clone https://github.com/shekhsahebali/Youtube-Channel-Scraping.git
cd Youtube-Channel-Scraping
```
- Download browser/ChromeDriver.

```sh
npx @puppeteer/browsers install chrome@145.0.7568.0
npx @puppeteer/browsers install chromedriver@145.0.7568.0
```
- mv Chromium file to (linux) 
```sh
mv chrome/linux-145.0.7568.0/chrome-linux64 chromium
mv chromedriver/linux-145.0.7568.0/chromedriver-linux64 chromiumdriver
rm -r chrome chromedriver
```
- mv Chromium file to (windows)
```sh
mv chrome/windows-145.0.7568.0/chrome-windows64 chromium
mv chromedriver/windows-145.0.7568.0/chromedriver-windows64 chromiumdriver
rm -r chrome chromedriver
```

- Install Library
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
or

```sh
uv pip install -r requirements.txt
```
### Run the Script
```sh
python3 main.py
```
or
```sh
uv run main.py
```
Done!!


## ⚠️ Legal Disclaimer

This project is for educational purposes only.
The scripts are not intended to be used on any website that prohibits automated data extraction.
Users are solely responsible for complying with website Terms of Service, robots.txt, and applicable laws.
The author does not encourage scraping copyrighted or restricted content.

