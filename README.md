# INDIAMART-SCRAPPED
This project is a Python-based web scraper designed to extract information about infrared sensors from IndiaMART. Using a combination of Selenium and BeautifulSoup, the scraper efficiently handles dynamic web pages and collects details such as product names, prices, seller information, and locations. The extracted data is saved as a CSV file for further analysis or reference. 
IndiaMART Infrared Sensor Data Scraper

This Python script automates the process of scraping product information for infrared sensors (or similar products) from the IndiaMART website. It utilizes Selenium for handling dynamic web pages and login procedures and BeautifulSoup for parsing the extracted HTML.
Features

    Logs into IndiaMART using a mobile number and OTP verification.
    Scrapes detailed product information:
        Product Name
        Price
        Address
        City
        Company Name
    Handles infinite scrolling by repeatedly clicking the "Show More Results" button.
    Saves the extracted data into an Excel file for easy access and analysis.

Prerequisites

    Python 3.7+

    Required Python Libraries:
        BeautifulSoup4
        Pandas
        Selenium
        OpenPyXL Install these with:

    pip install beautifulsoup4 pandas selenium openpyxl

    Firefox Browser: Ensure Firefox is installed on your system.

    GeckoDriver: Download the appropriate GeckoDriver for your Firefox version from here.

Setup

    Clone the repository or save the script file:

    git clone https://github.com/your-username/indiamart-scraper.git
    cd indiamart-scraper

    Update the script with the correct paths:
        GeckoDriver path:
        Replace webdriver_path in the script with the location of your downloaded GeckoDriver.
        Firefox binary path:
        Update firefox_binary_path with the path to your Firefox executable.

    Set your mobile number for login:
        Replace the mobile_number variable with your mobile number.

Usage

    Run the script:

    python indiamart_scraper.py

    The script will:
        Open IndiaMART and log in using the provided mobile number and OTP.
        Scrape product details for 20 minutes or until all results are fetched.
        Save the extracted data to an Excel file at the specified location.

    Locate the output file:
        Default output path: C:\Users\DELL\Documents\indiamart_product_data_with_company.xlsx

Error Handling

    If the script encounters an error during execution, it captures a screenshot for debugging. The screenshot is saved at C:\Users\DELL\Documents\error_screenshot.png.
    Ensure all required paths and elements are configured correctly.

Limitations

    The script relies on IndiaMART's current HTML structure. Changes to the website may require adjustments to the code.
    Scraping large amounts of data may trigger anti-scraping measures.

License

This project is licensed under the MIT License.
