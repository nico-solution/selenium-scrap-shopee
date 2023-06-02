from __future__ import print_function

from auth import spreadsheet_service

from auth import drive_service

def read_range():

    range_name = 'Sheet1!A1:H100'  # read an empty row for new data

    spreadsheet_id = 'spreadsheet id of the sheet to read from (In this case, the “Contacts” sheet)'

    result = spreadsheet_service.spreadsheets().values().get(

    spreadsheetId=spreadsheet_id, range=range_name).execute()

    rows = result.get('values', [])

    print('{0} rows retrieved.'.format(len(rows)))

    print('{0} rows retrieved.'.format(rows))

    return rows

def write_range(rows):

    spreadsheet_id = 'spreadsheet id of the sheet to write into (In this case, the “New Test Sheet” sheet)'  # get the ID of the existing sheet

    range_name = 'Sheet1!A1:H100'  # update the range in the existing sheet

    values = rows  # use the rows retrieved from the read_range function

    value_input_option = 'USER_ENTERED'

    body = {

        'values': values

    }

    result = spreadsheet_service.spreadsheets().values().update(

    spreadsheetId=spreadsheet_id, range=range_name,

    valueInputOption=value_input_option, body=body).execute()

    print('{0} cells updated.'.format(result.get('updatedCells')))

if __name__ == '__main__':

    rows = read_range()

    write_range(rows)