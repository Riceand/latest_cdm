from helper import is_empty, replace_space_in_name
from cdmlib import convert_pk, convert_column_type, join_list_space, \
  get_table_name, get_str_item, get_column_values, \
  TABLE_COLUMN, KEY, DATA_TYPE, join_list_comma_line, join_all_part, \
  FOLDER_CDM

FOLDER_DDL = FOLDER_CDM + '/DDL/'
SQL_DDL_START = 'CREATE OR REPLACE TABLE {{cdm_table_dataset}}.{}\n('
SQL_DDL_END = ');'

def gen_ddl_columns(columns, types, pks):
    results = []
    for i in range(len(columns)):
        if is_empty(columns[i]):
            continue
        str_pks = convert_pk(get_str_item(pks, i))
        str_types = convert_column_type(get_str_item(types, i))
        result = join_list_space([columns[i], str_types, str_pks])
        result = replace_space_in_name(result, ' ')
        results.append(result.strip())
    return results

def gen_ddl_sql(the_sheet):
    table_name = get_table_name(the_sheet)
    columns = get_column_values(the_sheet, TABLE_COLUMN)
    pks = get_column_values(the_sheet, KEY)
    types = get_column_values(the_sheet, DATA_TYPE)
    ddl_columns = gen_ddl_columns(columns, types, pks)
    str_columns = join_list_comma_line(ddl_columns)

    # str.format() See: https://pyformat.info
    # or: https://www.geeksforgeeks.org/python-format-function/
    # or CN: https://www.runoob.com/python/att-string-format.html
    start = SQL_DDL_START.format(table_name)
    end = SQL_DDL_END
    return join_all_part(start, str_columns, end)
