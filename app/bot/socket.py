from .handleMessage import messageHandler
from flask_socketio import SocketIO, join_room

def socketHandler(io, commands, config):
  @io.on('join')
  def Join(data):
    join_room(data)
    io.emit('sendMessage',{"data":""}, to=data)
  
  @io.on('sendMessage')
  def sendMessage(data):
    io.emit('sendMessage', data, to=data['room'])
  
  @io.on('recieveMessage')
  def handleMessage(data):
    room = data["room"]
    del data['room']
    message = data
#   message = {
#     "text": data['text'],
#     "reply_to": data['reply_to'],
#     "id": data['id']
#   }
    messageHandler(io, message, room, commands, config)