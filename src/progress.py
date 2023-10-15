'''
 # @ Author: Liaco
 # @ Create Time: 2023-05-13 23:54:09
 # @ Modified by: Liaco
 # @ Modified time: 2023-09-10 18:13:43
 # @ Description:
    处理Excel文件(生成图片)
 '''
import os
import pandas as pd
import xlwings as xw


def progress(workbook, base_path):

    def clear_0(address):  # 清空小于0的值
        clear_range = workbook.sheets['处理'].range(f'{address}')
        for cell in clear_range:
            try:
                if int(cell.value) < 0:
                    cell.clear_contents()
            except ValueError:
                pass  # 这里跳过无法转换为整数的值

    def sort(address_list: list[str], sort_col_index: int, ascending: bool):
        """对指定的单元格进行排序"""
        for address in address_list:
            sheet = workbook.sheets['处理']
            data_range = sheet.range(address)
            df = data_range.options(
                pd.DataFrame, index=False, header=False).value
            df_sorted = df.sort_values(
                by=df.columns[sort_col_index], ascending=ascending)
            data_range.value = df_sorted.values

    def copy_paste(sheet_names, address_list):
        for i in range(len(sheet_names)):
            copy_range = workbook.sheets[sheet_names[i]].range('A1:D50')
            paste_range = workbook.sheets['处理'].range(address_list[i])
            copy_range.copy()
            paste_range.paste(paste='values')

    def select_range():
        workbook.sheets['处理'].range('D55').expand('down').copy()
        workbook.sheets['处理'].range('V55').paste()
        select_top = workbook.sheets['处理'].range('D55').expand('down').count
        select_top += 54
        workbook.sheets['处理'].range(f'A55:A{select_top}').copy()
        workbook.sheets['处理'].range('U55').paste()

        workbook.sheets['处理'].range('N55').expand('down').copy()
        workbook.sheets['处理'].range('Y55').paste()
        select_top = workbook.sheets['处理'].range('N55').expand('down').count
        select_top += 54
        workbook.sheets['处理'].range(f'K55:K{select_top}').copy()
        workbook.sheets['处理'].range('X55').paste()

        workbook.sheets['处理'].range('U55:Y105').copy()
        workbook.sheets['处理'].range('U1').paste()

    def to_png(address, name):
        cells = workbook.sheets['处理'].range(f'{address}').expand()
        cells.columns.autofit()
        cells.to_png(name)

    ws = workbook.sheets['处理']
    sheet_names = ['澳模', "港模", '澳模', "港模"]
    address_list = ['A1', 'K1', 'A55', 'K55']
    copy_paste(sheet_names, address_list)
    address_list = ['A56:D104', 'K56:N104']
    sort(address_list, 3, 0)
    for address in ['D2:D50', 'N2:N50', 'D56:D104', 'N56:N104']:
        clear_0(address)
    select_range()
    sum_range = f"D2:D50"
    ws.range('D51').formula = f"=SUM({sum_range})"
    ws.range('D51').copy()
    ws.range('N51').paste()
    ws.range('A51:S52').copy()
    ws.range('A105').paste()
    address_list = ['U2:V50', 'X2:Y50']
    sort(address_list, 0, 1)

    to_png('A1', './Output/Pic/澳门总（序号）.png')
    to_png('K1', './Output/Pic/香港总（序号）.png')
    to_png('U1', './Output/Pic/澳门局部（序号）.png')
    to_png('X1', './Output/Pic/香港局部（序号）.png')
    to_png('A55', './Output/Pic/澳门总（收入）.png')
    to_png('K55', './Output/Pic/香港总（收入）.png')
    to_png('U55', './Output/Pic/澳门局部（收入）.png')
    to_png('X55', './Output/Pic/香港局部（收入）.png')


if __name__ == '__main__':
    app = xw.App(visible=True, add_book=False)
    workbook = app.books.open(r'../Output/Tables/Table_1007.xlsx')
    progress(workbook)
