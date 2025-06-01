import os
import sys
import csv
import time
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv, find_dotenv

def load_environment_variables():
    """
    Load environment variables from a .env file and verify their presence.
    """
    dotenv_path = find_dotenv()
    if not dotenv_path:
        print("Error: .env file not found.")
        sys.exit(1)
    load_dotenv(dotenv_path=dotenv_path, override=True)
    print(f".env file loaded from: {dotenv_path}")

    linkedin_email = os.getenv("LINKEDIN_EMAIL")
    linkedin_password = os.getenv("LINKEDIN_PASSWORD")

    if not linkedin_email:
        print("Error: LINKEDIN_EMAIL is not set in the environment variables.")
        sys.exit(1)
    if not linkedin_password:
        print("Error: LINKEDIN_PASSWORD is not set in the environment variables.")
        sys.exit(1)

    print("Environment variables loaded successfully.")
    return linkedin_email, linkedin_password

def initialize_webdriver():
    """
    Initialize the Selenium WebDriver with desired options.
    """
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    print("Initializing the WebDriver...")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def login_linkedin(driver, email, password):
    """
    Automate the LinkedIn login process.
    """
    print("Navigating to LinkedIn login page...")
    driver.get("https://www.linkedin.com/login")

    try:
        print("Locating the email input field...")
        email_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        if email_input is None:
            print("Error: Email input field not found.")
            driver.quit()
            sys.exit(1)
        print("Entering email...")
        email_input.send_keys(email)

        print("Locating the password input field...")
        password_input = driver.find_element(By.ID, "password")
        if password_input is None:
            print("Error: Password input field not found.")
            driver.quit()
            sys.exit(1)
        print("Entering password...")
        password_input.send_keys(password)

        print("Submitting login form...")
        password_input.submit()

        # Wait for the homepage to load by checking for the presence of the search bar
        print("Waiting for the homepage to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "global-nav-search"))
        )
        print("Login successful!\n")
    except TimeoutException:
        print("Login failed: Timeout while trying to log in.\n")
        driver.quit()
        sys.exit(1)
    except NoSuchElementException as e:
        print(f"Login failed: {e}\n")
        driver.quit()
        sys.exit(1)

def process_input_csv(file_path):
    """
    Read the input CSV file and return a list of LinkedIn profile URLs.
    """
    profile_urls = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row.get('profile_url')
                if url:
                    profile_urls.append(url.strip())
        print(f"Loaded {len(profile_urls)} profile URLs from {file_path}")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        sys.exit(1)
    return profile_urls

def download_image(image_url, save_path):
    """
    Download an image from the given URL and save it to the specified path.
    """
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image downloaded and saved to {save_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image: {e}")

def scrape_profile(driver, profile_url):
    """
    Navigate to a LinkedIn profile and extract the name and profile image URL.
    """
    print(f"Processing profile: {profile_url}")
    driver.get(profile_url)
    time.sleep(5)  # Wait for the page to load

    try:
        # Locate the div containing the profile image
        photo_wrapper = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pv-top-card__non-self-photo-wrapper"))
        )
        if photo_wrapper is None:
            print("Error: Photo wrapper not found.")
            return

        # Locate the img tag within the photo wrapper
        profile_image = photo_wrapper.find_element(By.TAG_NAME, "img")
        if profile_image is None:
            print("Error: Profile image not found.")
            return

        name = profile_image.get_attribute("title")
        image_url = profile_image.get_attribute("src")

        if name and image_url:
            print(f"Name: {name}")
            print(f"Image URL: {image_url}")

            # Create a safe filename
            parsed_url = urlparse(profile_url)
            profile_id = os.path.basename(parsed_url.path)
            filename = f"{name.replace(' ', '_')}_{profile_id}.jpg"
            save_path = os.path.join("profile_images", filename)

            # Ensure the directory exists
            os.makedirs("profile_images", exist_ok=True)

            # Download the image
            download_image(image_url, save_path)
        else:
            print("Could not extract name or image URL.")
    except TimeoutException:
        print("Timeout while trying to load profile elements.")
    except Exception as e:
        print(f"Error processing profile: {e}")

def main():
    linkedin_email, linkedin_password = load_environment_variables()
    driver = initialize_webdriver()

    try:
        login_linkedin(driver, linkedin_email, linkedin_password)

        # Process input.csv
        input_file = "input.csv"
        profile_urls = process_input_csv(input_file)

        for url in profile_urls:
            scrape_profile(driver, url)
            time.sleep(2)  # Be polite and avoid hitting LinkedIn too hard

    finally:
        print("Closing the WebDriver...")
        driver.quit()

if __name__ == "__main__":
    main()
