from __future__ import print_function
import time

from auth import spreadsheet_service
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# import undetected_chromedriver as uc
from auth import drive_service
chrome_options = Options()
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-extensions')

chrome_options.add_argument(
    "user-data-dir=C:\\Users\\miro\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument('--profile-directory=Profile 2')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)
# driver = uc.Chrome()
values = []


def read_range():

    range_name = 'Sheet1!D2:D5000'  # read an empty row for new data

    spreadsheet_id = '17IaVsJOqLdBtT3UYChbOdr0pPXr7nUT43T0Qs1ck3nU'

    result = spreadsheet_service.spreadsheets().values().get(

        spreadsheetId=spreadsheet_id, range=range_name).execute()

    rows = result.get('values', [])
    for url in rows:
        if url != "":
            if url[0].find('seller') == -1 and url[0].find("product") == -1:
                driver.get(url[0])
                elem = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-briefing")))
                priceElement = elem.find_element_by_class_name("pqTwkA")
                price = priceElement.text
                soldElement = elem.find_element_by_class_name("P3CdcB")
                sold = soldElement.text
                quantity_element = driver.find_element_by_xpath(
                    "//div[contains(text(), 'Quantity')]/following-sibling::div")
                text = quantity_element.text
                stock = text.split()[0]
                values.append([price, sold, stock])
            values.append(["", "", ""])

    # print('{0} rows retrieved.'.format(len(rows)))

    # print(priceElement)

    # print('{0} rows retrieved.'.format(rows))

    return


def write_range():

    # get the ID of the existing sheet
    spreadsheet_id = '17IaVsJOqLdBtT3UYChbOdr0pPXr7nUT43T0Qs1ck3nU'

    range_name = 'Sheet1!E2:G5000'  # update the range for three rows

    # values = [

    #     ['John', 'John', '20'],  # new row of data

    #     ['Jane', 'Doe', '30'],  # new row of data

    #     ['Bob', 'Smith', '25'],  # new row of data

    # ]

    value_input_option = 'USER_ENTERED'

    body = {

        'values': values

    }

    result = spreadsheet_service.spreadsheets().values().update(

        spreadsheetId=spreadsheet_id, range=range_name,

        valueInputOption=value_input_option, body=body).execute()

    print('{0} cells updated.'.format(result.get('updatedCells')))


if __name__ == '__main__':

    read_range()
    write_range()
    driver.close()
