import os
import sys

import xlsxwriter


def save_to_xlsx(data, excel_file_name):
    try:
        if os.path.exists(excel_file_name):
            os.remove(excel_file_name)
        workbook = xlsxwriter.Workbook(excel_file_name, options={'remove_timezone': True})
        worksheet = workbook.add_worksheet()
        for i, key in enumerate(data):
            col = i + 1
            worksheet.write(0, 0, 'S.No')
            worksheet.write(0, col, key)
            for index, value in enumerate(data[key]):
                # print(index, value)
                row = index + 1
                worksheet.write(row, 0, row)
                if key == 'date':
                    print(value)
                    format2 = workbook.add_format({'num_format': 'dd/mm/yy hh:mm AM/PM'})
                    worksheet.write(row, col, value, format2)
                else:
                    worksheet.write(row, col, value)
        workbook.close()
        return "success"
    except Exception as e:
        print("Exception in saveexslx", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        return "Error"
