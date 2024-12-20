import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import random
import time
from bs4 import BeautifulSoup


# List of User-Agent strings
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
]

# Randomly select a User-Agent
selected_user_agent = random.choice(user_agents)

# Chrome options setup
chrome_options = Options()
# chrome_options.add_argument("--headless=new")  # Run in headless mode
chrome_options.add_argument(f"user-agent={selected_user_agent}")
# chrome_options.add_argument(f"--proxy-server={proxy}")

# WebDriver setup
driver_path = "chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(30)
actions = ActionChains(driver)

try:
    # TikTok product URL
    url = "https://shop-my.tiktok.com/view/product/1729536094887576896?close_page=1"
    driver.get(url)

    # Random delay before interacting
    time.sleep(random.uniform(2, 5))
    # time.sleep(300)

    # Wait for the dialog to appear (if necessary)
    dialog_close_button = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, "cancel-sUFBJq"))
    )
    time.sleep(2)
    dialog_close_button.click()

    # # Incremental scroll to handle lazy-loaded content
    # scroll_pause_time = 3
    # last_height = driver.execute_script("return document.body.scrollHeight")

    # while True:
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #     time.sleep(scroll_pause_time)

    #     # Check if the page height has changed
    #     new_height = driver.execute_script("return document.body.scrollHeight")
    #     if new_height == last_height:
    #         break
    #     last_height = new_height

    dialog_close2_button = WebDriverWait(driver, 10).until(
        ec.presence_of_element_located((By.CLASS_NAME, "text-color-UIText3"))
    )
    time.sleep(2)
    dialog_close2_button.click()

    select_button = driver.find_element(By.XPATH, '//*[@id="scroll-body"]')
    actions.move_to_element(select_button).perform()
    time.sleep(2)
    select_button.click

    choose_button = WebDriverWait(driver, 10).until(
    ec.element_to_be_clickable((By.CLASS_NAME, "itemDescContainer-jnaffc"))
    )
    choose_button.click()

    # click_button = WebDriverWait(driver, 20).until(
    # ec.element_to_be_clickable((By.CLASS_NAME, "selected-Bl6_d4 border-StZJcn"))
    # )
    # click_button.click()

    # Save page source
    with open("page_source.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    print("Page source saved to 'page_source.html'")

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # # Locate the image container
    # image_container = driver.find_element(By.XPATH, '//*[@id="module_item_gallery_1"]')

    # # Find all image elements inside the container
    # img_elements = image_container.find_elements(By.TAG_NAME, 'img')

    src_list = []

    actions = ActionChains(driver)

    # for img in img_elements:
    #     #Hover over the image
    #     actions.move_to_element(img).perform()
    #     time.sleep(1.5)

    #     #Get the updated src attribute
    #     current_src = img.get_attribute('src')

    #     #Avoid Duplicates
    #     if current_src and current_src not in src_list:
    #         src_list.append(current_src)

    # Print all captured sources
    # print("Captured Image Sources:")
    # for i, src in enumerate(src_list):
    #     print(f"{i + 1}: {src}")

    # for i, url in enumerate(src_list):
    #     try:
    #         response = requests.get(url, stream=True)
    #         # Raise HTTPError for bad responses
    #         response.raise_for_status()
    #         with open("sample_data/lazada{}.jpg".format(i), "wb") as f:
    #             for chunk in response.iter_content(1024):
    #                 f.write(chunk)
    #         print(f"Downloaded: lazada{i}.jpg")
    #     except Exception as e:
    #         print(f"Failed to download image {i}: {e}")


    try:
        price = soup.find("div", class_="price-w1xvrw").get_text(strip=True)
    except Exception:
        price = "N/A"

    try:
        summary = soup.find("h1", class_="title-v0v6fK").get_text(strip=True)
    except Exception:
        summary = "N/A"

    try:
        colour_elements = soup.find_all("div", class_="specifications-vkOVJ_")
        colours = [element.get_text(strip=True) for element in colour_elements]
    except Exception:
        colours = ["N/A"]

    try:
        feature_elements = soup.find_all("div", class_="text-nu9zLI textnomarginbottom-Y3gzIE textnomargintop-ghqYmI")
        features = [element.get_text(strip=True) for element in feature_elements]
    except Exception:
        features = ["N/A"]

    # try:
    #     highlight_title = soup.find("h2", class_="pdp-mod-section-title outer-title").get_text(strip=True)
    # except Exception:
    #     highlight_title = "N/A"

    # try:
    #     highlight_element = soup.find("div", class_="pdp-product-detail")
    #     highlight_elements = highlight_element.find("ul")
    #     highlights = [element.get_text(strip=True) for element in highlight_elements]
    # except Exception:
    #     highlights = ["N/A"]

    # Print scraped data
    print("Price:", price)
    print("Summary:", summary)
    print("Colours:", colours)
    print("Product Feature:", features)
    # print("Highlight Title:", highlight_title)
    # print("Highlights: ", highlights)

finally:
    # Close the WebDriver
    driver.quit()
