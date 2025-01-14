from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import os
import time

# Paths
webdriver_path = r"C:\Users\DELL\Downloads\geckodriver-v0.35.0-win32\geckodriver.exe"
firefox_binary_path = r"C:\Program Files\Mozilla Firefox\firefox.exe"
target_url = "https://dir.indiamart.com/search.mp?ss=infrared+lamp+sesor&v=4&mcatid=&catid=&qu-cx=1&tags=res:RC4|ktp:N0|stype:attr=1&mtp:S&wc:3&qr_nm:gd&cs:8855&com-cf:nl&ptrs:na&mc:34431&cat:628&qry_typ:P&lang:en&flavl:0-1&..."

# Mobile number for login
mobile_number = "6261277633"

# Validate paths
if not os.path.exists(webdriver_path):
    raise FileNotFoundError(f"GeckoDriver not found at: {webdriver_path}")
if not os.path.exists(firefox_binary_path):
    raise FileNotFoundError(f"Firefox binary not found at: {firefox_binary_path}")

# Set up Selenium WebDriver
service = Service(webdriver_path)
options = Options()
options.binary_location = firefox_binary_path

try:
    driver = webdriver.Firefox(service=service, options=options)
    print("Firefox WebDriver initialized successfully.")
except Exception as e:
    raise Exception("Failed to initialize Firefox WebDriver.") from e

# Step 1: Open the target URL and handle sign-in
try:
    driver.get(target_url)
    print(f"Target URL loaded: {target_url}")

    # Wait for the sign-in prompt
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Sign In"))
    )
    sign_in_button.click()
    print("Sign In button clicked.")
    time.sleep(3)  # Allow the login page to load

    # Enter the mobile number
    mobile_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "mobile"))
    )
    mobile_field.send_keys(mobile_number)
    print(f"Mobile number {mobile_number} entered.")

    # Wait for the "Send OTP" button and click it
    otp_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "passwordbtn1"))  # Button to send OTP
    )
    otp_button.click()
    print("OTP button clicked. Waiting for OTP input fields...")

    # Wait for the OTP input fields and verify login success
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.ID, "after_verified"))  # Login success indicator
    )
    print("Login successful. Proceeding to scrape results...")
except Exception as e:
    # Take a screenshot for debugging
    screenshot_path = r"C:\Users\DELL\Documents\error_screenshot.png"
    driver.save_screenshot(screenshot_path)
    print(f"Saved screenshot to {screenshot_path} for debugging.")
    driver.quit()
    raise Exception("Failed during the login process.") from e

# Step 2: Scrape product names, prices, addresses, cities, and company names
product_names = []
product_prices = []
product_addresses = []
product_cities = []
company_names = []

def extract_page_data():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cards = soup.find_all('div', class_='card')  # Locate all product cards

    for card in cards:
        # Extract product name
        product_name_tag = card.find('a', class_='cardlinks')  # Product name tag
        product_name = product_name_tag.get_text(strip=True) if product_name_tag else 'No Name'

        # Extract product price
        price_tag = card.find('p', class_='price')  # Price tag
        product_price = price_tag.get_text(strip=True) if price_tag else 'Price Not Available'

        # Extract address and city
        address_div = card.find('div', class_='dib pr to-txt-gn')  # Address div
        city_tag = address_div.find('span', class_='elps elps1') if address_div else None
        full_address_tag = address_div.find('p', class_='tac wpw') if address_div else None

        product_city = city_tag.get_text(strip=True) if city_tag else 'City Not Available'
        product_address = full_address_tag.get_text(strip=True) if full_address_tag else 'Address Not Available'

        # Extract company name
        company_tag = card.find('a', {'data-click': '^CompanyName'})  # Company name tag
        company_name = company_tag.get_text(strip=True) if company_tag else 'Company Not Available'

        # Append data
        product_names.append(product_name)
        product_prices.append(product_price)
        product_addresses.append(product_address)
        product_cities.append(product_city)
        company_names.append(company_name)

# Step 3: Click "Show More Results" for 20 minutes
start_time = time.time()
duration = 20 * 60  # 20 minutes in seconds

try:
    while time.time() - start_time < duration:
        extract_page_data()  # Scrape current page data

        # Continuously wait for and click "Show More Results"
        try:
            show_more_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Show more results')]"))
            )
            show_more_button.click()
            print("Clicked 'Show more results'.")
            time.sleep(3)  # Wait for the next batch of results to load
        except Exception:
            print("No 'Show More Results' button currently visible. Retrying...")
            time.sleep(5)  # Wait before retrying
except Exception as e:
    print(f"An error occurred during scraping: {e}")

# Save data to Excel
data = {
    'Product Name': product_names,
    'Price': product_prices,
    'Address': product_addresses,
    'City': product_cities,
    'Company Name': company_names
}
df = pd.DataFrame(data)
output_path = r'C:\Users\DELL\Documents\indiamart_product_data_with_company.xlsx'
df.to_excel(output_path, index=False)
print(f"Data successfully saved to {output_path}")

# Close the WebDriver
driver.quit()

