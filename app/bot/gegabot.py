import secrets
import mimetypes

class Util:
  def get_mimetype(self, file_path: str) -> str:
    mime_type, encoding = mimetypes.guess_type(file_path)
    if mime_type:
      return mime_type.split('/')[0]
    else:
      return 'invalid'
  def fix_buttons(self, buttons: dict | list):
    if isinstance(buttons, dict):
      buttons = [buttons]
    if not isinstance(buttons, list):
      return None
    return buttons
  
  
class Bot(Util):
  def __init__(self, room: str, socket, config, commands):
    self._io = socket
    self._room = room
    
    self.prefix = config.bot.prefix
    self.commands = commands
    self.developer = config.DEVELOPER
  def sendMessage(self, datos, reply_to=None) -> dict:
    messageID = f"MSG-{secrets.token_hex(20)}"
    data = {
      "id": messageID,
      "data": {},
      "reply": reply_to
    }
    if type(datos) == str:
      data["data"] = {"body":datos}
    if type(datos) == dict:
      if "body" in datos:
        data["data"]["body"] = datos["body"]
      if "attachment" in datos:
        base = datos["attachment"]
        if type(base) == dict:
          house1 = list()
          house2 = base
          if 'type' not in base:
            house2['type'] = self.get_mimetype(base['src'])
          house1.append(house2)
          data["data"]["attachment"] = house1
        if type(base) == list:
          bahay1 = list()
          for attch in base:
            bahay2 = attch
            if 'type' not in attch:
              bahay2['type'] = self.get_mimetype(attch['src'])
            bahay1.append(bahay2)
          data["data"]["attachment"] = bahay1
      if "button" in datos:
        btn_fix = self.fix_buttons(datos['button'])
        if btn_fix:
          data["data"]["button"] = btn_fix
    self._io.emit('sendMessage', data, to=self._room)
    return {
      "id": messageID,
      "data": datos
    }
  def replyMessage(self, data: dict, id=None) -> None:
    # Use sendMessage() instead
    if not id:
      print("ERROR: bobo wala kang nilagay naessage id")
    return self.sendMessage(data, id)
  def unsendMessage(self, messageID):
    self._io.emit('unsendMessage', {
      "id": messageID
    }, to=self._room)
  def errorMessage(self, message, id=None):
    self.sendMessage(f":danger-color[:icon[fa-solid fa-warning]] {message}", reply_to=id)