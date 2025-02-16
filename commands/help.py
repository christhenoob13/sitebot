def get_page(commands, PREFIX, page=1):
  if page > len(commands):
    return f":danger-color[:icon[fa-solid fa-warning]] Page not found, total command page is {len(commands)}"
  message = ":icon[fa-solid fa-gear] :bold[Command Lists]\n"
  message += "━━━━━━━━━━━━━━━━━━━━━\n"
  for cmd in commands[page-1]:
    message += f":bold[{PREFIX}{cmd['name']}] - {cmd['description']}\n"
  message += "━━━━━━━━━━━━━━━━━━━━━\n"
  message += f"'{PREFIX}help <page>' to see other command.\n"
  message += f":bold[PAGE]: ({page}/{len(commands)})"
  return message

def get_all(commands, PREFIX):
  message = ":icon[fa-solid fa-gear] :bold[Command list]\n"
  message += "━━━━━━━━━━━━━━━━━━━━━\n"
  for command in commands:
    for cmd in command:
      message += f":bold[{PREFIX}{cmd['name']}] - {cmd['description']}\n"
  message += "━━━━━━━━━━━━━━━━━━━━━\n"
  return message

def get_command(commands,PREFIX, name):
  for command in commands:
    for cmd in command:
      if cmd['name'] == name:
        message = f"━━━━━━━━( :bold[{name}] )━━━━━━━━\n"
        message += f":bold[Credits]: {cmd['credits']}\n"
        message += f":bold[Usage]: {cmd['usage']}\n"
        message += f":bold[Description]: {cmd['description']}"
        return message
  return f":danger-color[:icon[fa-solid fa-warning]] Command '{name}' not found."

def help(bot, data):
  PREFIX = bot.prefix
  COMMANDS = bot.commands
  _cmdArray = [{
    "name": v.get('name'),
    "def": v.get('def'),
    "usage": v.get('usage', f"{PREFIX}{v['name']}") or f"{config.PREFIX}{v['name']}",
    "description": v.get('description', 'No description!') or 'No discription!',
    "credits": v.get('credits')
  } for key,v in COMMANDS.items()]
  
  commands = [_cmdArray[i:i+10] for i in range(0, len(_cmdArray), 10)]
  args = data.args
  isPage = True
  
  if not args:
    return bot.sendMessage(get_page(commands, PREFIX))
  if args.lower() == 'all':
    return bot.sendMessage(get_all(commands, PREFIX))
  
  _01j = [str(i) for i in range(1,11)]
  for char in list(args):
    if char not in _01j:
      isPage = False
  
  if isPage:
    return bot.sendMessage(get_page(commands, PREFIX, page=int(args)))
  else:
    return bot.sendMessage(get_command(commands, PREFIX, args))

config = {
  "name": 'help',
  "def": help,
  "credits": "Greegmon",
  "usage": "{p}help [none|all|<page>|<cmdName>]",
  "description": "Get all command list/usage"
}