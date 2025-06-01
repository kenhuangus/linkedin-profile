
# LinkedIn Profile Image Scraper

## 📌 Description

This Python script automates the process of:

* Logging into LinkedIn using provided credentials.
* Reading a list of LinkedIn profile URLs from an `input.csv` file.
* Navigating to each profile.
* Extracting the user's name and profile image URL.
* Downloading and saving the profile image locally.

**Note:** Ensure compliance with LinkedIn's [Terms of Service](https://www.linkedin.com/legal/user-agreement) when using this script.

---

## ✅ Prerequisites

* **Python 3.11** installed on your system.
* A **LinkedIn account** with valid login credentials.
* **Google Chrome** browser installed.
* **ChromeDriver** compatible with your Chrome version.
* **Git** installed (optional, for cloning the repository).

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

If you haven't already, clone this repository:

```bash
git clone https://github.com/kenhuangus/linkedin-profile-image-scraper.git
cd linkedin-profile-image-scraper
```

Alternatively, download the repository as a ZIP file and extract it.

### 2. Create and Activate a Virtual Environment with Python 3.11

#### On Windows:

```bash
# Create a virtual environment named 'venv' using Python 3.11
py -3.11 -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

#### On macOS and Linux:

```bash
# Create a virtual environment named 'venv' using Python 3.11
python3.11 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

*If you have multiple Python versions installed, ensure that Python 3.11 is correctly referenced. You can specify the full path to the Python 3.11 executable if necessary.*

### 3. Upgrade pip (Optional but Recommended)

```bash
pip install --upgrade pip
```

### 4. Install Required Dependencies

```bash
pip install selenium webdriver-manager python-dotenv requests

```


### 5. Set Up Environment Variables

Create a `.env` file in the project root directory and add your LinkedIn credentials:

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
```

*Replace `your_email@example.com` and `your_password` with your actual LinkedIn login credentials.*

---

## 🚀 Running the Script

1. Ensure your virtual environment is activated.

2. Prepare the `input.csv` file in the project directory with the following structure:

   ```csv
   profile_url
   https://www.linkedin.com/in/example1/
   https://www.linkedin.com/in/example2/
   ```

   *Each row should contain a valid LinkedIn profile URL.*

3. Run the script:

   ```bash
   python main.py
   ```

   *Replace `main.py` with the actual filename of your script if different.*

4. The script will:

   * Log into LinkedIn.
   * Read profile URLs from `input.csv`.
   * Navigate to each profile.
   * Extract the user's name and profile image URL.
   * Download and save the profile image in the `profile_images` directory.

---

## 📝 Notes and Best Practices

* **Respect LinkedIn's Terms of Service:** Use this script responsibly and ensure compliance with LinkedIn's [Terms of Service](https://www.linkedin.com/legal/user-agreement).

* **Avoid Account Lockouts:** Excessive automated requests can lead to account restrictions. Introduce delays between requests if necessary.

* **Update ChromeDriver:** Ensure that your ChromeDriver version matches your installed Chrome browser version. You can download the appropriate version from [ChromeDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads).

* **Handle Exceptions:** The script includes basic exception handling. Monitor the console output for any errors or issues during execution.

* **Deactivate Virtual Environment:** After completing your tasks, deactivate the virtual environment:

  ```bash
  deactivate
  ```

---

If you encounter any issues or have questions, feel free to open an issue or contribute to the project.

---
