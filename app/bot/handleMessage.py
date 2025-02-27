from box import Box
from .gegabot import Bot

def messageHandler(socket, datos, roam, commands, config):
  bot = Bot(roam, socket, config, commands)
  txt = datos['text']
  if not txt.startswith(config.bot.prefix):
    return
  if len(txt) == 1:
    return
  
  text = txt[1:].split(' ', 1)
  cmd = text[0]
  pretty_args = text[1] if len(text) > 1 else ''
  args = " ".join(pretty_args.split()) if pretty_args else ''
  if cmd.lower() not in commands:
    return bot.sendMessage(f":danger-color[:icon[fa-solid fa-warning]] Command '{cmd.lower()}' not found.")

  function = commands[cmd.lower()]["def"]
  data = Box({
    "cmd": cmd.lower(),
    "pretty_args": pretty_args,
    "args": args,
    "messageId": datos["id"],
    "reply_to": datos['reply_to'] if datos['reply_to'] else {},
    "sender": datos['sender'],
    "prefix": config.bot.prefix,
    "developer": config.DEVELOPER
  })
  function(bot, data)