from __future__ import print_function
from random import randint
import time
import re
from datetime import datetime
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
from_row_number=2
to_row_number=100
# driver = uc.Chrome()
values = []


def scrap_shopee(url,driver,variation_product,before_URL):
    variationArray=[]
    if before_URL !=url:  
        driver.get(url)
        wait = WebDriverWait(driver, 30)
    variationElement = driver.find_elements(By.CLASS_NAME, "product-variation")
    if len(variationElement) > 0:
        for element in variationElement:
            if variation_product[0] == element.text:
                
                element.click()
                # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pqTWkA')))
                priceElement = driver.find_elements(By.CLASS_NAME, "pqTWkA")
                price = priceElement[0].text
                # wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_44qnta')))
                productTitleElement = driver.find_elements(By.CLASS_NAME, "_44qnta")
                productTitle=productTitleElement[-1].find_element(By.XPATH, ".//span[last()]").text
                # moqElement = driver.find_elements(By.CLASS_NAME, "I+H1Co")
                # print(moqElement,"moqtext")
                # if len(moqElement)>0 :
                #     moqText=moqElement[0].text
                #     # moq = [int(s) for s in moqText.split() if s.isdigit()][0]
                #     moq = re.findall(r'\d+', moqText)[0] 

                # else:
                #     moq=""

                elements = driver.find_elements(By.TAG_NAME,"div")
                moq=""
                for element in elements:
                    if "This item has a Minimum Purchase Quantity (MPQ) requirement of" in element.text:
                        moq=re.findall(r'\d+', element.text)[0]
                        
                # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.flex.items-center._6lioXX > div:last-child')))
                
                piece_available_element = driver.find_elements(By.CSS_SELECTOR, ".flex.items-center._6lioXX > div:last-child")[0].text
                
                # stock=[int(s) for s in piece_available_element.split() if s.isdigit()][0]
                stock = re.findall(r'\d+', piece_available_element)[0] 
                variation=variation_product[0]
                now = datetime.now()

                current_time = now.strftime("%H:%M %m-%d-%Y")
                return ([productTitle,variation,price, stock, moq,current_time])
             
    else: 
            variationArray=[]
            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_44qnta')))
            productTitleElement = driver.find_elements(By.CLASS_NAME, "_44qnta")
            productTitle=productTitleElement[-1].find_element(By.XPATH, ".//span[last()]").text
            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pqTWkA')))
            priceElement = driver.find_elements(By.CLASS_NAME, "pqTWkA")
            price = priceElement[0].text
            # moqElement = driver.find_elements(By.CLASS_NAME, "I+H1Co")
            # if len(moqElement)>0 :
            #     moqText=moqElement[0].text
            #     # moq = [int(s) for s in moqText.split() if s.isdigit()][0]
            #     moq = re.findall(r'\d+', moqText)[0]
            # else:
            #     moq=""

            elements = driver.find_elements(By.TAG_NAME,"div")
            moq=""
            for element in elements:
                if "This item has a Minimum Purchase Quantity (MPQ) requirement of" in element.text:
                    moq=re.findall(r'\d+', element.text)[0]
                    
            # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.flex.items-center._6lioXX > div:last-child')))

            piece_available_element = driver.find_elements(By.CSS_SELECTOR, ".flex.items-center._6lioXX > div:last-child")[0].text
         
            
            # stock=[int(s) for s in piece_available_element.split() if s.isdigit()][0]
            stock = re.findall(r'\d+', piece_available_element)[0] 
            variation=' '.join(variationArray)
            now = datetime.now()

            current_time = now.strftime("%H:%M %m-%d-%Y")
            return([productTitle,variation,price, stock, moq,current_time])
    

def read_range():

    range_name = 'Sheet1!K{}:K{}' 
    variationRange_name='Sheet1!C{}:C{}'
    spreadsheet_id = '17IaVsJOqLdBtT3UYChbOdr0pPXr7nUT43T0Qs1ck3nU'

    result = spreadsheet_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name.format(from_row_number,to_row_number)).execute()
    variationResult=spreadsheet_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=variationRange_name.format(from_row_number,to_row_number)).execute()
    rows = result.get('values', [])
    variations=variationResult.get('values', [])
    time.sleep(randint(3,5))
   
    for index, url in enumerate(rows):
        print(url)
        if url != []:
            if "shopee.sg" in url[0]:    
                if url[0].find('seller') == -1 and url[0].find("product") == -1:
                        result=scrap_shopee(url[0],driver,variations[index],rows[index-1][0])
                        write_range(from_row_number+index,result) 
                elif url[0].find('seller') == -1 and url[0].find("product") >= 0:
                        result=scrap_shopee(url[0],driver,variations[index],rows[index-1][0])
                        write_range(from_row_number+index,result) 
                else:         
                    now = datetime.now()
                    current_time = now.strftime("%H:%M %m-%d-%Y")
                    write_range(from_row_number+index,["", "", "","","",current_time])
            else:
                now = datetime.now()
                current_time = now.strftime("%H:%M %m-%d-%Y")
                write_range(from_row_number+index,["", "", "","","",current_time])
        else:
            now = datetime.now()
            current_time = now.strftime("%H:%M %m-%d-%Y")
            write_range(from_row_number+index,["", "", "","","",current_time]) 
          
    driver.close()
    return

def write_range(rowNumber,data):
    print(rowNumber,data,"write_range")

    # get the ID of the existing sheet
    spreadsheet_id = '17IaVsJOqLdBtT3UYChbOdr0pPXr7nUT43T0Qs1ck3nU'

    range_name = 'Sheet1!L{}:Q{}'  # update the range for three rows

    

    value_input_option = 'USER_ENTERED'

    body = {

        'values': [data]

    }

    result = spreadsheet_service.spreadsheets().values().update(

        spreadsheetId=spreadsheet_id, range=range_name.format(rowNumber,rowNumber),

        valueInputOption=value_input_option, body=body).execute()

    print('{0} cells updated.'.format(result.get('updatedCells')))
    return


if __name__ == '__main__':

    read_range()
    write_range()
    
