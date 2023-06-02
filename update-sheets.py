from __future__ import print_function

from auth import spreadsheet_service

from auth import drive_service

def read_range():

    range_name = 'Sheet1!A1:H10'  # retrieve data from existing sheet

    spreadsheet_id = 'your_spreadsheetID'

    result = spreadsheet_service.spreadsheets().values().get(

    spreadsheetId=spreadsheet_id, range=range_name).execute()

    rows = result.get('values', [])

    print('{0} rows retrieved.'.format(len(rows)))

    print('{0} rows retrieved.'.format(rows))

    return rows

def write_range():

    spreadsheet_id = 'your_spreadsheetID'  # get the ID of the existing sheet

    range_name = 'Sheet1!A2:H2'  # the range to update in the existing sheet

    values = [['Ben', 'Stiller', 50, 'Male', 'New Jersey', 'USA', '98989898989', 'j11292@example.com']]  # new row of data

    value_input_option = 'USER_ENTERED'

    body = {

        'values': values

    }

    result = spreadsheet_service.spreadsheets().values().update(

        spreadsheetId=spreadsheet_id, range=range_name,

        valueInputOption=value_input_option, body=body).execute()

    print('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == '__main__':

    write_range()

    read_range()