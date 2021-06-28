import os
import re
import logging

def is_windows():
  return os.name == 'nt'

def exist_path(path_name):
  return os.path.exists(path_name)

def mkdir(path_name):
  if exist_path(path_name):
    return False
  os.mkdir(path_name, 0o755)
  return True

def mkdirs(path_name):
  if exist_path(path_name):
    return False
  os.makedirs(path_name, 0o755)
  return True

def rmdir(path_name):
  return os.rmdir(path_name)

def rmdirs(path_name):
  return os.removedirs(path_name)

def is_empty(something):
  something = something.strip() if isinstance(something, str) else something
  return not something or (isinstance(something, str) and len(something) <=0)

def remove_not_word_char(s):
    return re.sub(r'\W+', '', s)

# 将多个空格替换为 repl，并删除两边的空格
def replace_space_in_name(name, repl):
    return re.sub(r'\s+', repl, name)

def strip_list(array):
    return list(map(lambda s: s.strip(), array))

def to_word_list(array):
    return list(map(remove_not_word_char, array))

def split_cell_value(cell_value):
    ary = re.split(r'\W+', cell_value.strip())
    return to_word_list(ary)
