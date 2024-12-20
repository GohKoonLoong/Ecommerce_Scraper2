from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument(f"user-agent={selected_user_agent}")

# WebDriver setup
driver_path = "chromedriver.exe"
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.maximize_window()
driver.implicitly_wait(10)
actions = ActionChains(driver)
src_list = []
sku_texts = []

try:
    # Shopee product URL
    url = "https://shopee.com.my/Men's-new-fashion-waterproof-silicone-silicone-sports-watch-i.188678203.24621331727?sp_atk=d48c0e69-3b4e-4f96-a183-56fe30b673f6&xptdk=d48c0e69-3b4e-4f96-a183-56fe30b673f6"
    driver.get(url)
    time.sleep(5)

    language_button = driver.find_element(By.XPATH,'//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button')
    time.sleep(1.5)
    language_button.click()


    # Save page source
    with open("page_source.html", "w", encoding="utf-8") as file:
        file.write(driver.page_source)

    print("Page source saved to 'page_source.html'")

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    try:
        price = soup.find("span", class_="pdp-price").get_text(strip=True)
    except Exception:
        price = "N/A"

    try:
        name = soup.find("h1", class_="pdp-mod-product-badge-title").get_text(strip=True)
    except Exception:
        name = "N/A"

    try:
        variation_container = driver.find_element(By.XPATH, '//*[@id="module_sku-select"]/div/div/div/div/div[2]')
        sku_images = variation_container.find_elements(By.TAG_NAME, 'span')
        # sku_images = driver.find_elements(By.CLASS_NAME, "sku-variable-img wrap")

        for img_wrap in sku_images:
            actions.move_to_element(img_wrap).perform()
            time.sleep(0.5)
            sku_text = driver.find_element(By.CLASS_NAME, "sku-name").text
            sku_texts.append(sku_text)
    except Exception:
       sku_texts=["N/A"]

    try:
        highlight_element = soup.find("div", class_="pdp-product-detail")
        highlight_elements = highlight_element.find("ul")
        highlights = [li.find("div").get_text(strip= True) for li in highlight_elements.find_all("li") if li.find("div")]
    except Exception:
        highlights = ["N/A"]

    try:
        table = soup.find("table")
        columns = table.find_all('p')
        details = [element.get_text(strip=True) for element in columns]
    except Exception:
        details = ["N/A"]

    try:
        spec_element = soup.find("div", class_ ="pdp-mod-specification")
        spec_elements = spec_element.find("ul")
        specs = [li.find("div").get_text(strip= True) for li in spec_elements.find_all("li") if li.find("div")]
    except Exception:
        specs = ["N/A"]

    print("Images: ", src_list)
    print("Price:", price)
    print("Variation: ", sku_texts)
    print("Name:", name)
    print("Highlights: ", highlights)
    print("Details: ", details)
    print("Specifications: ", specs)

finally:
    # Close the WebDriver
    driver.quit()

