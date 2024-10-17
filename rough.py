import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager as CM

def scrape(instagram_account=None):
    if not instagram_account:
        instagram_account = "nitish_naik_04"  # Default account name
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument("--log-level=3")
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36')

    # Initialize WebDriver
    bot = webdriver.Chrome(options=options)
    instagram_url = f'https://www.instagram.com/{instagram_account}/'

    print(f'[Info] - Scraping profile: {instagram_account}...')
    try:
        bot.get(instagram_url)
        time.sleep(3.5)  # Wait for the page to load

        # Get total followers
        followers_span = bot.find_element(By.XPATH, "//a[contains(@href, '/followers/')]/span")
        total_followers = followers_span.get_attribute('title')

        # Get total following
        following_span = bot.find_element(By.XPATH, "//a[contains(@href, '/following/')]/span")
        total_following = following_span.text
        
        # Get total posts
        posts_span = bot.find_element(By.XPATH, "//a[contains(@href, '/')][1]/span")
        total_posts = posts_span.text

        # Return the data
        return {
            'followers': total_followers,
            'following': total_following,
            'posts': total_posts
        }

    except NoSuchElementException as e:
        print(f'[Error] - An element was not found: {e}')
        return None
    finally:
        bot.quit()  # Ensure the browser is closed

if __name__ == '__main__':
    if len(sys.argv) > 1:
        account_name = sys.argv[1]
    else:
        account_name = None

    result = scrape(account_name)
    
    if result:
        print(f"[Result] - Followers: {result['followers']}, Following: {result['following']}, Posts: {result['posts']}")
    else:
        print("[Result] - Could not retrieve profile information.")
