import logging
import re

from helper import is_empty, replace_space_in_name, \
    remove_not_word_char, to_word_list, split_cell_value
from cdmlib import convert_pk, convert_column_type, \
    get_table_name, get_str_item, get_column_values, \
    TABLE_COLUMN, KEY, DATA_TYPE, join_list_comma_line, join_all_part, \
    FOLDER_CDM, filter_not_empty_columns, remove_remark, find_first_col, \
    get_table_column_values, find_cell_pos, get_columns_by_title, \
    convert_column_type

HUB_TABLE = 'Table'
HUB_FIELD = 'Field'
FOLDER_INSERT = FOLDER_CDM + '/INSERT/'
SQL_INSERT_START = 'INSERT {{cdm_table_dataset}}.{}\n('
SQL_INSERT_MID = ')\nSELECT'
SQL_INSERT_END = 'FROM {{cdm_raw_dataset}}.{};'

# 超过 32 个字符的 field 描述，就不处理了，由人工解决。
MAX_PARSE_LIMIT = 32

def get_field_str(field_column, field_type):
    default = '0' if field_type == 'NUMERIC' else '\'\''
    return default if field_column == '' else field_column

def as_column(insert_column, field_column, data_type):
    is_simple = len(field_column) < 32
    field_type = convert_column_type(data_type)
    field_str = get_field_str(field_column, field_type)
    cast_str = 'CAST({} AS {})'.format(field_str, field_type)
    from_str = cast_str if is_simple else 'NULL'
    return '{} AS {}'.format(from_str, insert_column)

def get_hub_table_names(the_sheet):
    hub_table_cols = get_columns_by_title(the_sheet, HUB_TABLE)
    hub_table_str = find_first_col(hub_table_cols, HUB_TABLE)
    logging.debug(hub_table_str)
    return split_cell_value(hub_table_str)

def gen_insert_columns(the_sheet):
    return get_table_column_values(the_sheet)

def get_field_columns(the_sheet):
    columns = get_column_values(the_sheet, HUB_FIELD)
    if not columns: return None
    return list(filter_not_empty_columns(columns))

def fn_map_i_fields(i):
    def map_i_fields(field_column):
        ary_fields = split_cell_value(field_column)
        # logging.debug('ary_fields: ', ary_fields)
        # 有时会出现少于个数，无法对应的情况，则返回 \'\'
        return get_str_item(ary_fields, i)
    return map_i_fields

def gen_as_columns(insert_columns, field_columns, data_types, i):
    if not field_columns: return None
    map_i_fields = fn_map_i_fields(i)
    logging.debug(field_columns)
    fields = list(map(map_i_fields, field_columns))
    return list(map(as_column, insert_columns, fields, data_types))

def gen_insert_sql(the_sheet, hub_table):
    table_name = get_table_name(the_sheet)

    insert_columns = gen_insert_columns(the_sheet)
    field_columns = get_field_columns(the_sheet)

    hub_table_names = get_hub_table_names(the_sheet)
    i = hub_table_names.index(hub_table)

    # data_types = get_data_types(the_sheet)
    data_types = get_column_values(the_sheet, DATA_TYPE)

    as_columns = gen_as_columns(insert_columns, field_columns, data_types, i)

    str_insert_columns = join_list_comma_line(insert_columns)
    str_select_columns = join_list_comma_line(as_columns)

    start = SQL_INSERT_START.format(table_name)
    end = SQL_INSERT_END.format(table_name)
    return join_all_part(start, str_insert_columns, SQL_INSERT_MID, \
      str_select_columns, end)
