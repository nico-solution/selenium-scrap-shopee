from __future__ import print_function
from random import randint
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
chrome_options.add_argument('--profile-directory=Profile 1')

driver = webdriver.Chrome(options=chrome_options)

# driver = uc.Chrome()
values = []


def read_range():

    range_name = 'Sheet1!D2:D10'  # read an empty row for new data

    spreadsheet_id = '17IaVsJOqLdBtT3UYChbOdr0pPXr7nUT43T0Qs1ck3nU'

    result = spreadsheet_service.spreadsheets().values().get(

        spreadsheetId=spreadsheet_id, range=range_name).execute()

    rows = result.get('values', [])
    for url in rows:
        if url[0] != "":
            if url[0].find('seller') == -1 and url[0].find("product") == -1:
                    driver.get(url[0])
                    time.sleep(randint(7,10))
                    variation=[]
                 
                    # elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-briefing")))
                    productTitleElement = driver.find_elements(By.CLASS_NAME, "_44qnta")
                    productTitle=productTitleElement[-1].find_element(By.XPATH, "./div[last()]").text
                    
                    priceElement = driver.find_elements(By.CLASS_NAME, "pqTWkA")
                    price = priceElement[0].text
                    elements = driver.find_elements(By.CLASS_NAME, "_44qnta")
                    variationElement = driver.find_elements(By.CLASS_NAME, "product-variation")
                    if len(variationElement) > 0:
                         for element in variationElement:
                            variation.append(element.text)
                    else: variation=[]
                   
                    moqElement = driver.find_element(By.CLASS_NAME, "I+H1Co").text
                    moq = [int(s) for s in moqElement.split() if s.isdigit()][0]
                    # quantity_element = driver.find_elements(By.CLASS_NAME,"//div[contains(text(), 'Quantity')]/following-sibling::div")
                    # text = quantity_element[0].text
                    # stock = text.split()[0]
                    piece_available_element = driver.find_element(By.CSS_SELECTOR, ".flex.items-center._6lioXX > div:last-child")
                    
                    stock=[int(s) for s in piece_available_element.split() if s.isdigit()][0]
                    values.append([productTitle,variation,price, stock, moq]) 
                    print(productTitle,variation,price, stock, moq)

            elif url[0].find('seller') == -1 and url[0].find("product") >= 0:
                    driver.get(url[0])
                    time.sleep(randint(7,10))
                    variation=[]
                   
                    # elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-briefing")))
                    productTitleElement = driver.find_elements(By.CLASS_NAME, "_44qnta")
                    productTitle=productTitleElement[-1].find_element(By.XPATH, "./div[last()]").text
                    
                    priceElement = driver.find_elements(By.CLASS_NAME, "pqTWkA")
                    price = priceElement[0].text
                    elements = driver.find_elements(By.CLASS_NAME, "_44qnta")
                    variationElement = driver.find_elements(By.CLASS_NAME, "product-variation")
                    if len(variationElement) > 0:
                         for element in variationElement:
                            variation.append(element.text)
                    else: variation=[]
                   
                    moqElement = driver.find_element(By.CLASS_NAME, "I+H1Co").text
                    moq = [int(s) for s in moqElement.split() if s.isdigit()][0]
                    # quantity_element = driver.find_elements(By.CLASS_NAME,"//div[contains(text(), 'Quantity')]/following-sibling::div")
                    # text = quantity_element[0].text
                    # stock = text.split()[0]
                    piece_available_element = driver.find_element(By.CSS_SELECTOR, ".flex.items-center._6lioXX > div:last-child")
                    
                    stock=[int(s) for s in piece_available_element.split() if s.isdigit()][0]
                    values.append([productTitle,variation,price, stock, moq]) 
                    print(productTitle,variation,price, stock, moq)

        else:
             values.append(["", "", "","",""])

    # print('{0} rows retrieved.'.format(len(rows)))

    # print(priceElement)

    # print('{0} rows retrieved.'.format(rows))

    return


def write_range():

    # get the ID of the existing sheet
    spreadsheet_id = '17IaVsJOqLdBtT3UYChbOdr0pPXr7nUT43T0Qs1ck3nU'

    range_name = 'Sheet1!E2:I10'  # update the range for three rows

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
