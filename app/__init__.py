from flask import Flask, render_template
from flask_socketio import SocketIO
from dotenv import load_dotenv
from box import Box
import os
import json

try:
  config = json.load(open('config.json', 'r'))
except FileNotFoundError:
  print("\033[41mERROR: \033[0mFile 'config.json' not found.")

def myapp():
  from .bot.socket import socketHandler
  from .bot.loadCommands import commands
  from .views import view
  from .cmdRoutes import cmd
  from .api import api
  
  app = Flask(__name__,
    template_folder=os.path.abspath('frontend'),
    static_folder=os.path.abspath('frontend/static'),
  )
  app.secret_key = ":(){:|:&};"
  socket = SocketIO(app)
  load_dotenv()
  socketHandler(
    socket,
    commands(Box(config)),
    Box(config)
  )
  
  @app.errorhandler(404)
  def not_found(e):
    return render_template('404.html'),404
  
  app.register_blueprint(api, url_prefix='/api')
  app.register_blueprint(view)
  app.register_blueprint(cmd)
  
  return [socket, app]