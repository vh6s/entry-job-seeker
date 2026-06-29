import gspread
from credentials.spreadsheet import SPREADSHEET_URL, WORKSHEET_NAME

gc = gspread.service_account(filename="credentials/service_account.json")
sh = gc.open_by_key(SPREADSHEET_URL).worksheet(WORKSHEET_NAME)