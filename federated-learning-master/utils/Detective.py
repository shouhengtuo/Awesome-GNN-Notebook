from colorama import Fore, Style
import re
import inspect
import torch
def varname(p):
  for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
    m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
      return m.group(1)
def tensor_deteciteve(variable):
  try:
    name = varname(variable)
    print(Fore.GREEN + name,": ", type(variable), ": ", variable.shape)
    print(Style.RESET_ALL)
  except AttributeError:
    print(Fore.RED + "AttributeError: Wrong Variable Type")
    exit()
  else:
      None
