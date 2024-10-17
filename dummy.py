import time
import os
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
    """Save credentials to a text file."""
    with open('credentials.txt', 'w') as file:
        file.write(f"{username}\n{password}")

def load_credentials():
    """Load credentials from a text file."""
    if not os.path.exists('credentials.txt'):
        return None

    with open('credentials.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) >= 2:
            return lines[0].strip(), lines[1].strip()

    return None

def prompt_credentials():
    """Prompt user for their Instagram credentials."""
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    save_credentials(username, password)
    return username, password

def login(bot, username, password):
    """Log into Instagram."""
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
    time.sleep(5)

def scrape_followers(bot, username, user_input):
    """Scrape followers for a given Instagram username."""
    bot.get(f'https://www.instagram.com/{username}/')
    time.sleep(3.5)
    WebDriverWait(bot, TIMEOUT).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/followers')]"))).click()
    time.sleep(2)
    print(f"[Info] - Scraping followers for {username}...")

    users = set()
    scroll_count = 0
    reached_page_end = False
    last_height = bot.execute_script("return document.body.scrollHeight")
    
    while not reached_page_end:
        time.sleep(2)
        followers = bot.find_elements(By.XPATH, "//a[contains(@href, '/')]")
        
        for i in followers:
            href = i.get_attribute('href')
            if href:
                users.add(href.split("/")[-2])  # get the username
            
        scroll_count += 1
        screenshot_filename = f"{username}_followers_scroll_{scroll_count}.png"
        bot.save_screenshot(screenshot_filename)
        print(f"[Info] - Screenshot taken: {screenshot_filename}")
        
        # Scroll down to load more followers
        ActionChains(bot).send_keys(Keys.END).perform()
        time.sleep(1)
        
        new_height = bot.execute_script("return document.body.scrollHeight")
        if last_height == new_height:
            reached_page_end = True
        else:
            last_height = new_height

    print(f"[Info] - Total followers scraped for {username}: {len(users)}")
    with open(f'{username}_followers.txt', 'a') as file:
        file.write('\n'.join(users) + "\n")
    print(f"[Info] - Saved followers to {username}_followers.txt")

def scrape():
    """Main function to scrape followers."""
    credentials = load_credentials()

    if credentials is None:
        username, password = prompt_credentials()
    else:
        username, password = credentials

    try:
        with open(f"{username}_followers.txt", 'r') as file:
            user_input = int(file.read().strip())
    except FileNotFoundError:
        user_input = int(input('[Required] - How many followers do you want to scrape (100-2000 recommended): '))

    usernames = input("Enter the Instagram usernames you want to scrape (separated by commas): ").split(",")

    service = Service(CM().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    mobile_emulation = {
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/90.0.1025.166 Mobile Safari/535.19"
    }
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    bot = webdriver.Chrome(service=service, options=options)
    bot.set_page_load_timeout(15)  # Set the page load timeout to 15 seconds
    bot.maximize_window()
    login(bot, username, password)

    for user in usernames:
        user = user.strip()
        scrape_followers(bot, user, user_input)

    bot.quit()

if __name__ == '__main__':
    TIMEOUT = 15
    scrape()
