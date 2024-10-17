# import time
# import os
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager as CM
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.chrome.service import Service

# def save_credentials(username, password):
#     with open('credentials.txt', 'w') as file:
#         file.write(f"{username}\n{password}")

# def load_credentials():
#     if not os.path.exists('credentials.txt'):
#         return None

#     with open('credentials.txt', 'r') as file:
#         lines = file.readlines()
#         if len(lines) >= 2:
#             return lines[0].strip(), lines[1].strip()

#     return None

# def prompt_credentials():
#     username = input("Enter your Instagram username: ")
#     password = input("Enter your Instagram password: ")
#     save_credentials(username, password)
#     return username, password

# def login(bot, username, password):
#     bot.get('https://www.instagram.com/accounts/login/')
#     time.sleep(1)

#     # Check if cookies need to be accepted
#     try:
#         element = bot.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div[2]/button")
#         element.click()
#     except NoSuchElementException:
#         print("[Info] - Instagram did not require to accept cookies this time.")

#     print("[Info] - Logging in...")
#     username_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
#     password_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

#     username_input.clear()
#     username_input.send_keys(username)
#     password_input.clear()
#     password_input.send_keys(password)

#     login_button = WebDriverWait(bot, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
#     login_button.click()
#     time.sleep(5)  # Give time for the login process to complete

# def scrape_followers(bot, username):
#     bot.get(f'https://www.instagram.com/{username}/')
#     time.sleep(3.5)
#     WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))).click()
#     time.sleep(2)
#     print(f"[Info] - Scraping followers for {username}...")

#     users = set()
#     scroll_count = 0
#     user_count = 0  # Counter for scraped users

#     while True:
#         # Collect followers
#         followers = bot.find_elements(By.XPATH, "//a[contains(@href, '/')]")
#         for i in followers:
#             if i.get_attribute('href'):
#                 user_handle = i.get_attribute('href').split("/")[3]
#                 users.add(user_handle)
#                 user_count += 1  # Increment user count

#                 # Take screenshot every 10 users
#                 if user_count % 10 == 0:
#                     screenshot_filename = f"{username}_followers_users_{user_count // 10}.png"
#                     bot.save_screenshot(screenshot_filename)
#                     print(f"[Info] - Screenshot taken: {screenshot_filename}")

#         # Scroll down
#         ActionChains(bot).send_keys(Keys.END).perform()
#         time.sleep(2)  # Allow time for the new followers to load

#         # Check if we've reached the end of the list
#         new_height = bot.execute_script("return document.body.scrollHeight")
#         bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom
#         time.sleep(2)  # Wait for new content to load
#         current_height = bot.execute_script("return document.body.scrollHeight")
        
#         if new_height == current_height:
#             break  # Exit loop if we've reached the end of the list

#         scroll_count += 1

#     print(f"[Info] - Total followers scraped: {len(users)}")
#     # Optionally save users to a file
#     # with open(f'{username}_followers.txt', 'w') as file:
#     #     file.write('\n'.join(users) + "\n")

# def scrape():
#     credentials = load_credentials()

#     if credentials is None:
#         username, password = prompt_credentials()
#     else:
#         username, password = credentials

#     usernames = input("Enter the Instagram usernames you want to scrape (separated by commas): ").split(",")

#     service = Service()
#     options = webdriver.ChromeOptions()
#     # options.add_argument("--headless")  # Uncomment for headless mode
#     options.add_argument('--no-sandbox')
#     options.add_argument("--log-level=3")
#     mobile_emulation = {
#         "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
#     options.add_experimental_option("mobileEmulation", mobile_emulation)

#     bot = webdriver.Chrome(service=service, options=options)
#     bot.set_page_load_timeout(15)  # Set the page load timeout to 15 seconds
#     bot.maximize_window()
#     login(bot, username, password)

#     for user in usernames:
#         user = user.strip()
#         scrape_followers(bot, user)

#     bot.quit()

# if __name__ == '__main__':
#     TIMEOUT = 15
#     scrape()






































































import time
import os
from fpdf import FPDF
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

def save_credentials(username, password):
    with open('credentials.txt', 'w') as file:
        file.write(f"{username}\n{password}")

def load_credentials():
    if not os.path.exists('credentials.txt'):
        return None

    with open('credentials.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[0].strip(), lines[1].strip()

    return None

def prompt_credentials():
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    save_credentials(username, password)
    return username, password

def login(bot, username, password):
    bot.get('https://www.instagram.com/accounts/login/')
    time.sleep(1)

    # Check if cookies need to be accepted
    try:
        element = bot.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div[2]/button")
        element.click()
    except NoSuchElementException:
        print("[Info] - Instagram did not require to accept cookies this time.")

    print("[Info] - Logging in...")
    username_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password_input = WebDriverWait(bot, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username_input.clear()
    username_input.send_keys(username)
    password_input.clear()
    password_input.send_keys(password)

    login_button = WebDriverWait(bot, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    login_button.click()
    time.sleep(5)  # Give time for the login process to complete

def scrape_followers(bot, username, pdf):
    bot.get(f'https://www.instagram.com/{username}/')
    time.sleep(3.5)
    WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))).click()
    time.sleep(2)
    print(f"[Info] - Scraping followers for {username}...")

    users = set()

    # Scroll and scrape logic
    while True:
        # Collect followers
        followers = bot.find_elements(By.XPATH, "//a[contains(@href, '/')]")
        for i in followers:
            if i.get_attribute('href'):
                user_handle = i.get_attribute('href').split("/")[3]
                users.add(user_handle)

        # Take a screenshot after scrolling
        screenshot_filename = f"{username}_followers_users_{len(users) // 10}.png"
        bot.save_screenshot(screenshot_filename)
        print(f"[Info] - Screenshot taken: {screenshot_filename}")

        # Add the screenshot to the PDF
        pdf.add_page()
        pdf.image(screenshot_filename, x=10, y=10, w=190)  # Adjust size as needed

        # Scroll down smoothly
        for _ in range(5):  # Adjust the range for more or fewer scrolls
            ActionChains(bot).send_keys(Keys.END).perform()
            time.sleep(3)  # Allow time for the new followers to load

        # Check if we've reached the end of the list
        new_height = bot.execute_script("return document.body.scrollHeight")
        time.sleep(3)  # Wait for new content to load
        bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to the bottom
        time.sleep(3)  # Wait for new content to load
        current_height = bot.execute_script("return document.body.scrollHeight")
        time.sleep(3)
        if new_height == current_height:
            break  # Exit loop if we've reached the end of the list

    print(f"[Info] - Total followers scraped: {len(users)}")

def generate_pdf_report(pdf, username):
    pdf.output(f"{username}_followers_report.pdf")
    print(f"[Info] - PDF report generated: {username}_followers_report.pdf")

def scrape():
    credentials = load_credentials()

    if credentials is None:
        username, password = prompt_credentials()
    else:
        username, password = credentials

    usernames = input("Enter the Instagram usernames you want to scrape (separated by commas): ").split(",")

    service = Service()
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment for headless mode
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"}
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(service=service, options=options)
    bot.set_page_load_timeout(15)  # Set the page load timeout to 15 seconds
    bot.maximize_window()
    login(bot, username, password)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for user in usernames:
        user = user.strip()
        scrape_followers(bot, user, pdf)

    generate_pdf_report(pdf, username)

    bot.quit()

if __name__ == '__main__':
    TIMEOUT = 15
    scrape()
