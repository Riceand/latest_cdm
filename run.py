import logging

from cdmlib import mkdirs, create_file, get_table_name, \
    get_sheet, read_file, set_logger

from gen_ddl import FOLDER_DDL, gen_ddl_sql
from gen_view import FOLDER_VIEW, gen_view_sql
from gen_insert import FOLDER_INSERT, gen_insert_sql, get_hub_table_names

set_logger(logging.DEBUG)

MAP_FOLDER_GEN_FN = {
    FOLDER_DDL: gen_ddl_sql,
    FOLDER_VIEW: gen_view_sql,
    FOLDER_INSERT: gen_insert_sql
}

FOLDERS = MAP_FOLDER_GEN_FN.keys()

def gen_file(folder, table_name):
    mkdirs(folder)
    f = create_file(folder + table_name + '.sql')
    return f

def write_sql_file(folder, table_name, sql):
    f = gen_file(folder, table_name)
    f.write(sql)
    f.close()

def write_sql(file_name, sheet_name, folder):
    the_sheet = get_sheet(file_name, sheet_name)
    table_name = get_table_name(the_sheet)
    if folder == FOLDER_INSERT:
        hub_table_names = get_hub_table_names(the_sheet)
        for hub_table in hub_table_names:
            fd = folder + table_name + '/'
            sql = gen_insert_sql(the_sheet, hub_table)
            hub_file_name = table_name + '_' + hub_table
            write_sql_file(fd, hub_file_name, sql)
    else:
        sql = MAP_FOLDER_GEN_FN[folder](the_sheet)
        write_sql_file(folder, table_name, sql)

if __name__ == "__main__":
    logging.info('Start generate SQLs:')
    file_name = 'PhysicalModelNew.xlsx'
    sheets_file = read_file('test_sheets.txt')
    sheet_lines = sheets_file.readlines()

    # sheet_names = ['PARTY_REFERENCE', 'Party_relationship']
    for sheet_line in sheet_lines:
        sheet_name = sheet_line.strip()
        logging.info('Generating the "' + sheet_name + '" sheet.')
        for folder in FOLDERS:
            write_sql(file_name, sheet_name, folder)

    logging.info('Done! All SQL generated.')
