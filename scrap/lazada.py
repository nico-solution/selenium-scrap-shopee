
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support import expected_conditions as EC


def lazada_shopee(url,driver,variation_product,before_URL):
    variation=[]
    if before_URL !=url:  
        driver.get(url)
        # WebDriverWait(driver, 20)  
        
    try:    
        elum=WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'pdp-block__main-information-detail')))
        variationElements = elum.find_elements(By.CLASS_NAME, "sku-prop-content-header")
        if len(variationElements)>0:
            for variationElement in variationElements:
                    variation.append(variationElement.text)
        else:
            variation=[]
            
        productTitleElement = elum.find_elements(By.CLASS_NAME, "pdp-mod-product-badge-title")
        if len(productTitleElement)>0:
            productTitle=productTitleElement[0].text
        else:
            productTitle=''
        print(productTitle)
        priceElement = elum.find_elements(By.CLASS_NAME, "pdp-price_color_orange")
        if len(priceElement)>0:
            price = priceElement[0].text
        else:
            price=''
        piece_available_element = elum.find_elements(By.CLASS_NAME, "quantity-content-default")
        if len(piece_available_element)>0 and piece_available_element[0].text !="":
            stock = re.findall(r'\d+', piece_available_element[0].text)[0]  
        else:
            stock=""
        now = datetime.now()
        current_time = now.strftime("%H:%M %m-%d-%Y")

        return (productTitle,' '.join(variation),price,stock,"",current_time)
    except TimeoutException:
        elements = driver.find_elements(By.TAG_NAME,"h3")
        for element in elements:
            if "This product is no longer available" in element.text:
                now = datetime.now()
                current_time = now.strftime("%H:%M %m-%d-%Y")
                return ("","","","","",current_time)
        now = datetime.now()
        current_time = now.strftime("%H:%M %m-%d-%Y")
        return ("","","","","",current_time)    
    
    #     current_time = now.strftime("%H:%M %m-%d-%Y")
    #     return ("","","","","",current_time)
