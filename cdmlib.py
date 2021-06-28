import os
import re
import logging
import xlrd
from helper import mkdirs, exist_path, is_empty, replace_space_in_name

TABLE_NAME = 'Table Name'
TABLE_COLUMN = 'Table Column'
KEY = 'Key'
DATA_TYPE = 'Data Type'
ROW = 'row'
COL = 'col'
FOLDER_CDM = 'CDM'
FOLDER_INSERT = FOLDER_CDM + '/INSERT/'

def set_logger(level):
    logger = logging.getLogger()
    logger.setLevel(level)

def create_file(file_name):
    return open(file_name, 'w+')

def read_file(file_name):
    return open(file_name, 'r')

def remove_file(file_name):
    return os.remove(file_name)

def open_workbook(file_name):
    if exist_path(file_name):
        return xlrd.open_workbook(file_name)
    return None

def get_sheet(file_name, sheet_name):
    if exist_path(file_name):
        wb = xlrd.open_workbook(file_name)
        try:
            return wb.sheet_by_name(sheet_name)
        except Exception as e:
            logging.warning(e)
            return None
    return None

def get_row_values(the_sheet):
    the_range = list(range(the_sheet.nrows))
    return list(map(lambda i: the_sheet.row_values(i), the_range))

def get_col_values(the_sheet):
    the_range = list(range(the_sheet.ncols))
    return list(map(lambda i: the_sheet.col_values(i), the_range))

def find_index_in_list(ls, v):
    try:
        print("@@"*10,ls, v, "@@"*10)
        print(ls.index(v))
        return ls.index(v)
    except ValueError as ve:
        logging.debug(ve)
        return -1

def find_first_value_col(cols, title):
    if not cols:
        return -1
    start = False # 是否开始查找，从上往下只有找到 title 后，再开始找第一个不为空的值。
    i = 0
    for l in cols:
        if start and l.strip() != '':
            return i
        if l == title:
            start = True
        i = i + 1
    return -1

def find_first_col(cols, title):
    i = find_first_value_col(cols, title)
    return cols[i] if i >= 0 else ''

def find_cell_pos(sheet, cell_value):
    rows = get_row_values(sheet)
    print("!!!!!"*10, rows)
    x = -1
    y = -1
    for row in rows:
        x = x + 1
        f = find_index_in_list(row, cell_value)
        if f >= 0:
            y = f
            break
    return {ROW: x, COL: y}

def convert_table_column(cell_value):
    # 替换所有非字母、数字和下划线的字符为 '_'，如："(transaction) (part code) "
    tmp1 = re.sub(r'\W', '_', cell_value)
    # 删除开头和结尾的所有下划线，如："_transaction___part_code__"
    tmp2 = re.sub(r'^_+|_+$', '', tmp1)
    # 替换中间多个下划线为一个下划线，如："transaction___part_code"
    tmp3 = re.sub(r'_+', '_', tmp2)
    # 全部转换为大写，如："TRANSACTION_PART_CODE"
    return tmp3.upper()

def convert_column_type(cell_value):
    map_types = {
        'NUMBER': 'NUMERIC',
        'DATE': 'DATE',
        'TIME': 'TIME',
        'TIMESTAMP': 'TIMESTAMP',
    }
    return map_types.get(cell_value.strip().upper(), 'STRING')

def convert_pk(cell_value):
    has_pk = cell_value and cell_value.lower().find('pk') >= 0
    return 'NOT NULL' if has_pk else ''

def get_columns_by_title(the_sheet, title):
    pos = find_cell_pos(the_sheet, title) #{x:1,y:0}
    cols = get_col_values(the_sheet)
    x = pos[COL] # 0
    print("#" * 10, cols[x])
    return cols[x] if x >= 0 else None

def get_table_name(the_sheet):
    table_names = get_columns_by_title(the_sheet, TABLE_NAME)
    return replace_space_in_name(find_first_col(table_names, TABLE_NAME), '')

def get_column_all_values(the_sheet, title):
    cols = get_col_values(the_sheet)
    pos = find_cell_pos(the_sheet, title)
    x = pos[COL]
    return cols[x] if x >= 0 else None

def find_last_value_y(col_all_vals):
    last_index = len(col_all_vals)
    last = col_all_vals[last_index - 1]
    if last == '':
        col_all_vals.pop()
        return find_last_value_y(col_all_vals)
    return last_index

def get_column_values(the_sheet, title):
    col_all_vals = get_column_all_values(the_sheet, title)
    if not col_all_vals: return None
    y_from = find_first_value_col(col_all_vals, title)
    y_to = find_last_value_y(col_all_vals)
    return col_all_vals[y_from:y_to]

def get_table_column_values(the_sheet):
    columns = get_column_values(the_sheet, TABLE_COLUMN)
    if not columns: return None
    tables = filter_not_empty_columns(columns)
    return list(map(remove_remark, tables))

def get_str_item(array, i):
    return array[i] if i < len(array) else ''

def join_list(array, spliter):
    is_array = (isinstance(array, list) or isinstance(array, tuple))
    return spliter.join(array) if is_array else ''

def join_list_space(array):
    return join_list(array, ' ')

def join_list_comma_line(array):
    return join_list(array, ',\n')

def join_list_line(array):
    return join_list(array, '\n')

def filter_not_empty_columns(columns):
    fn_not_empty = lambda col: not is_empty(col)
    return None if not columns else filter(fn_not_empty, columns)

def remove_remark(table_column):
    match = re.match(r'([A-Z0-9_]+).*', table_column)
    return match.group(1)

def join_all_part(*strs):
    return join_list_line(strs)