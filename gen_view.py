from helper import is_empty
from cdmlib import get_table_name, get_table_column_values, \
  join_list_comma_line,  join_all_part, FOLDER_CDM, filter_not_empty_columns

FOLDER_VIEW = FOLDER_CDM + '/VIEW/'
SQL_VIEW_START = 'CREATE OR REPLACE VIEW {{cdm_view_dataset}}.{} AS SELECT'
SQL_VIEW_END = 'FROM {{cdm_table_dataset}}.{};'

def get_view_columns(the_sheet):
    return get_table_column_values(the_sheet)

def gen_view_sql(the_sheet):
    table_name = get_table_name(the_sheet)
    start = SQL_VIEW_START.format(table_name)
    end = SQL_VIEW_END.format(table_name)

    view_columns = get_view_columns(the_sheet)
    str_columns = join_list_comma_line(view_columns)

    return join_all_part(start, str_columns, end)
