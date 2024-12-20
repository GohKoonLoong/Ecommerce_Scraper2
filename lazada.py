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
chrome_options.add_argument("--headless=new")  # Run in headless mode
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
    # Lazada product URL
    url = "https://www.lazada.com.my/products/lenovo-ideapad-slim-3-15abr8-82xm00jbmj-156-fhd-laptop-arctic-grey-ryzen-5-7430u-16gb-512gb-ssd-ati-w11-hs-i4302814583-s24262780774.html"
    driver.get(url)
    time.sleep(30)

    # Incremental scroll to handle lazy-loaded content
    timeout = 30
    scroll_pause_time = 1
    last_height = driver.execute_script("return document.body.scrollHeight")
    start_time = time.time()

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        # Check if the page height has changed
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height or (time.time() - start_time) > timeout:
            break
        last_height = new_height

    try:
        # Locate view more button
        view_button = driver.find_element(By.XPATH, '//*[@id="module_product_detail"]/div/div/div[2]/button')
        actions.move_to_element(view_button).perform()

        #Sleep between every interaction
        time.sleep(1)
        view_button.click()
    except Exception:
        print("No Button")

    #Sleep between every interaction
    time.sleep(1)

    # Locate the image container
    image_container = driver.find_element(By.XPATH, '//*[@id="module_item_gallery_1"]')

    # Find all image elements inside the container
    img_elements = image_container.find_elements(By.TAG_NAME, 'img')

    for img in img_elements:
        # Hover over the image
        actions.move_to_element(img).perform()
        time.sleep(0.5)

        # Get the updated src attribute
        current_src = img.get_attribute('src')

        # Avoid Duplicates
        if current_src and current_src not in src_list:
            src_list.append(current_src)

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

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    formatted_html = soup.prettify()
    # Save page source
    with open("page_source.html", "w", encoding="utf-8") as file:
        file.write(formatted_html)

    print("Page source saved to 'page_source.html'")

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

