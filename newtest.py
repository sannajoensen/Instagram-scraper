import re
import urllib
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time



def recent_post_links(username, post_count=30):
    """
    With the input of an account page, scrape the 10 most recent posts urls
    Args:
    username: Instagram username
    post_count: default of 10, set as many or as few as you want
    Returns:
    A list with the unique url links for the most recent posts for the provided user
    """
    browser = webdriver.Chrome()
    browser.get("https://www.instagram.com/")
    accept = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))).click()
    username = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    username.clear()
    password.clear()
    username.send_keys("Bachelor_Projekt2020")
    password.send_keys("Bachelorprojekt2020")

    log_in = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    not_now = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    not_now2 = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

    search_box = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder = 'Search']")))

    search_box.clear()
    key_word = "@lilmiquela"
    search_box.send_keys(key_word)
    time.sleep(1)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)
    post = 'https://www.instagram.com/p/'
    post_links = []
    while len(post_links) < post_count:
        links = [a.get_attribute('href')
                 for a in browser.find_elements_by_tag_name('a')]
        for link in links:
            if post in link and link not in post_links:
                post_links.append(link)
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        time.sleep(1)
    else:
        browser.stop_client()
        return post_links[:post_count]


def find_hashtags(comment):
    """
    Find hastags used in comment and return them
    Args:
    comment: Instagram comment text
    Returns:
    a list or individual hashtags if found in comment
    """
    hashtags = re.findall('#[A-Za-z]+', comment)
    if (len(hashtags) > 1) & (len(hashtags) != 1):
        return hashtags
    elif len(hashtags) == 1:
        return hashtags[0]
    else:
        return ""


def find_mentions(comment):
    """
    Find mentions used in comment and return them
    Args:
    comment: Instagram comment text
    Returns:
    a list or individual mentions if found in comment
    """
    mentions = re.findall('@[A-Za-z]+', comment)
    if (len(mentions) > 1) & (len(mentions) != 1):
        return mentions
    elif len(mentions) == 1:
        return mentions[0]
    else:
        return ""


def insta_link_details(url):
    """
    Take a post url and return post details
    Args:
    urls: a list of urls for Instagram posts
    Returns:
    A list of dictionaries with details for each Instagram post, including link,
    post type, like/view count, age (when posted), and initial comment
    """
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    browser = Chrome(chrome_options=firefox_options)
    browser.get(url)
    try:
        # This captures the standard like count.
        likes = browser.find_element_by_xpath(
            """/html/body/div[1]/section/main/div/div/article/
                div[3]/section[2]/div/div/button/span""").text.split()[0]
        post_type = 'photo'
    except:
        # This captures the like count for videos which is stored
        likes = browser.find_element_by_xpath(
            """/html/body/div[1]/section/main/div/div/article/
                div[3]/section[2]/div/span/span""").text.split()[0]
        post_type = 'video'
    age = browser.find_element_by_css_selector('a time').text
    comment = browser.find_element_by_xpath(
        """/html/body/div[1]/section/main/div/div[1]/article/
        div[3]/div[1]/ul/div/li/div/div/div[2]/span""").text

    hashtags = find_hashtags(comment)
    mentions = find_mentions(comment)
    post_details = {'link': url, 'type': post_type, 'likes/views': likes,
                    'age': age, 'comment': comment, 'hashtags': hashtags,
                    'mentions': mentions}
    time.sleep(1)
    return post_details


def insta_url_to_img(url, filename="insta.jpg"):
    """
    Getting the actual photo file from an Instagram url
    Args:
    url: Instagram direct post url
    filename: file name for image at url
    Returns:
    image file, saved locally
    """
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    browser = Chrome(chrome_options=firefox_options)
    browser.get(url)
    try:
        image = browser.find_element_by_xpath(
            """/html/body/span/section/main/div/div/article/
                div[1]/div/div/div[1]/div[1]/img""").get_attribute('src').split(' ')[0]
        urllib.request.urlretrieve(image, filename)
    # If image is not a photo, print notice
    except:
        print("No image")
        
        
# Koden er fundet på: 
# jnawjux, 2020. Found on: https://github.com/jnawjux/web_scraping_corgis?fbclid=IwAR0AUgc_J5is-CtG2Pk7DWaqfix36paSxhgAewLxDm-69awxGV3cGZ82zUs [Sidst besøgt: 20.12.2020].
# Python Simplified, 2020: https://www.youtube.com/watch?v=iJGvYBH9mcY [Sidst besøgt: 20.12.2020].
