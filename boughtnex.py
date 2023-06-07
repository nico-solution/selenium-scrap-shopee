from __future__ import print_function
from datetime import datetime
from auth import spreadsheet_service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from auth import drive_service
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/scrap")
from shopee import scrap_shopee
chrome_options = Options()
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-extensions')

chrome_options.add_argument(
    "user-data-dir=C:\\Users\\miro\\AppData\\Local\\Google\\Chrome\\User Data")
chrome_options.add_argument('--profile-directory=Profile 1')

driver = webdriver.Chrome(options=chrome_options)
from_row_number=18
to_row_number=100
# driver = uc.Chrome()
values = []



def read_range():

    range_name = 'Sheet1!D{}:D{}' 
    variationRange_name='Sheet1!C{}:C{}'
    spreadsheet_id = '17IaVsJOqLdBtT3UYChbOdr0pPXr7nUT43T0Qs1ck3nU'

    result = spreadsheet_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name.format(from_row_number,to_row_number)).execute()
    variationResult=spreadsheet_service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=variationRange_name.format(from_row_number,to_row_number)).execute()
    rows = result.get('values', [])
    variations=variationResult.get('values', [])
   
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
            elif "lazada" in url[0]: 
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

    range_name = 'Sheet1!E{}:J{}'  # update the range for three rows

    

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
    
