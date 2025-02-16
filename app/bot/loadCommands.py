import importlib
import os
import types
import time

def commands(config):
  cmds = {}
  # *.py (excludes __init__.py)
  files = list(filter(lambda file: file.endswith('.py') and file!='__init__.py',os.listdir('./commands')))
  for file in files:
    filepath = f"commands.{os.path.splitext(file)[0]}"
    module = importlib.import_module(filepath)
    _config = getattr(module, 'config', None)
    if _config:
      name = _config.get('name')
      func = _config.get('def')
      if name and func:
        # check if command name have apaces
        if ' ' in name:
          print(f"\033[31mERROR: \033[34m({file}) \033[37mInvalid command name, it shouldn't have any spaces")
        # check the def instance
        elif not isinstance(func, types.FunctionType):
          print(f"\033[31mERROR: \033[34m({file}) \033[37mInvalid function")
        # check the name instance
        elif not isinstance(name, str):
          print(f"\033[31mERROR: \033[34m({file}) \033[37mCommand name should be string types")
        # check if command name already exist
        elif name in cmds:
          print(f"\033[31mERROR: \033[34m({file}) \033[37mCommand '{name}' already exist.")
        else:
          print(f"\033[34m({file}) \033[97m: Command Loaded - \033[33m{name}")
          cmds[name] = {
            "name": name,
            "def": func,
            "credits": _config.get('credits', 'Unknown') or 'Unknown',
            "description": _config.get('description').replace('{p}', config.bot.prefix) if _config.get('description') else 'No description!',
            "usage": _config.get('usage').replace('{p}', config.bot.prefix) if _config.get('usage') else config.bot.prefix + name
          }
  return cmds