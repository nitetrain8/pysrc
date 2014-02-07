import win32com
import win32com.client
import pythoncom



# excelapp = win32com.client.Dispatch("Excel.Application")
# excelapp.Visible = 1
# owb = excelapp.Workbooks.Add()
# worksheets = owb.Sheets(1)


def new_Excel():
    excel = win32com.client.Dispatch("Excel.Application")
    excel.visible = 1
    return excel

def Excel():
    try: 
        excel = win32com.client.GetActiveObject("Excel.Application")
    except:
        excel = new_Excel()
    return excel


