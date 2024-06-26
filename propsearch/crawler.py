import asyncio
import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Configuration properties
BASE_TSV = 'base_clean.tsv'
DATA_TSV = 'data.tsv'
PID_TSV = 'property_id.tsv'
PINFO_TSV = 'property_info.tsv'
ERRORS_LOG = 'errors.log'
DOWNLOAD_DIR = '/tmp/propsearch'
CHROMEDRIVER_PATH = './chromedriver'
WEB_DRIVER_POOL_SIZE = 1

# Selenium setup
chrome_options = Options()
chrome_options.add_experimental_option('prefs', {
    "download.default_directory": DOWNLOAD_DIR,  # Change default directory for downloads
    "download.prompt_for_download": False,  # To auto download the file
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True  # To enable safe browsing
})

service = Service(CHROMEDRIVER_PATH)

# Initialize a pool of WebDriver instances
async def _init_driver_pool():
    queue = asyncio.Queue()
    for _ in range(WEB_DRIVER_POOL_SIZE):
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        driver.get("https://travis.prodigycad.com/property-search")
        await queue.put(driver)
    return queue

async def _close_drivers(queue):
    while not queue.empty():
        driver = await queue.get()
        driver.quit()


def _append_line(source, message):
    with open(source, 'a') as error_log:
        error_log.write(message + '\n')


def process_address(driver, street_name, street_number):
    address = f"{street_number} {street_name}"
    print(f"processing {address}")

    try:
        def _clear_table_content():
            selector = driver.find_element(By.CSS_SELECTOR, 'input[value="2024"')
            selector = selector.find_element(By.XPATH, './..')
            selector.click()
            new_option = driver.find_element(By.CSS_SELECTOR, 'ul > li[data-value="2023"]')
            new_option.click()

            selector = driver.find_element(By.CSS_SELECTOR, 'input[value="2023"')
            selector = selector.find_element(By.XPATH, './..')
            selector.click()
            new_option = driver.find_element(By.CSS_SELECTOR, 'ul > li[data-value="2024"]')
            new_option.click()


        search_input = driver.find_element(By.ID, "searchInput")
        submit_button_xpath = '//*[@id="root"]/div/div/div/div[1]/div[2]/div/div[2]/div[2]/div[3]/div[2]/button'
        submit_button = driver.find_element(By.XPATH, submit_button_xpath)

        # clear table content
        _clear_table_content()

        # clear search input
        search_input.send_keys(Keys.COMMAND + "a")
        search_input.send_keys(Keys.DELETE)
        search_input.send_keys(address)
        submit_button.click()

        properties_selector = 'div[role="rowgroup"][class="ag-center-cols-container"] > div[role="row"]'
        properties = driver.find_elements(By.CSS_SELECTOR, properties_selector)
        if not properties:
            _append_line(ERRORS_LOG, f"{address} | NOT FOUND")

        for prop in properties:
            prop_type = prop.find_element(By.CSS_SELECTOR, 'div[role="gridcell"][col-id="propType"]').text
            if prop_type != 'R':
                _append_line(ERRORS_LOG, f"{address} | type: {prop_type}")
                continue
            prop_id = prop.find_element(By.CSS_SELECTOR, 'div[role="gridcell"][col-id="pid"] > a').text
            _append_line(PID_TSV, f'{street_name}\t{street_number}\t{prop_id}')

    except Exception as e:
        _append_line(ERRORS_LOG, f'{address} | {e.args[0]}')


async def task(queue, street_name, street_number):
    driver = await queue.get()
    try:
        process_address(driver, street_name, street_number)
    finally:
        await queue.put(driver)


async def main():
    queue = await _init_driver_pool()

    with open(BASE_TSV, 'r') as file:
        rows = csv.reader(file, delimiter='\t')  # street_name, street_number
        tasks = [task(queue, row[0], row[1]) for row in rows]

    await asyncio.gather(*tasks)
    await _close_drivers(queue)

if __name__ == "__main__":
    asyncio.run(main())
