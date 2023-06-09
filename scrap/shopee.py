
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from selenium.webdriver.common.by import By
import re



def scrap_shopee(url,driver,variation_product,before_URL):
    variationArray=[]
    if before_URL !=url:  
        driver.get(url)
        wait = WebDriverWait(driver, 40)
    variationElement = driver.find_elements(By.CLASS_NAME, "product-variation")
    variationSelectedElement = driver.find_elements(By.CLASS_NAME, "product-variation--selected")
    if len(variationElement) > 0  and len(variationSelectedElement) < 1:
        for element in variationElement:
            
            if variation_product[0] == element.text:
                is_disabled = element[0].get_attribute("disabled")
                if is_disabled:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M %m-%d-%Y")
                    return (["","","", "", "",current_time])
                else:
                    element.click()
                    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pqTWkA')))
                    priceElement = driver.find_elements(By.CLASS_NAME, "pqTWkA")
                    price = priceElement[0].text
                    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_44qnta')))
                    productTitleElement = driver.find_elements(By.CLASS_NAME, "_44qnta")
                    productTitle=productTitleElement[-1].find_element(By.XPATH, ".//span[last()]").text
                

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
            if len(variationSelectedElement)>0: 
                print(variationSelectedElement[0].text)
                variationArray=[variationSelectedElement[0].text]
            else:
                variationArray=[]
                  
            
            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_44qnta')))
            productTitleElement = driver.find_elements(By.CLASS_NAME, "_44qnta")
            productTitle=productTitleElement[-1].find_element(By.XPATH, ".//span[last()]").text
            # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pqTWkA')))
            priceElement = driver.find_elements(By.CLASS_NAME, "pqTWkA")
            price = priceElement[0].text

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
    