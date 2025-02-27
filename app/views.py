from flask import (
  Blueprint,
  render_template,
  session
)
from secrets import token_hex
view = Blueprint('view',__name__)

@view.route('/')
def root():
  sid = session.get('sid')
  if not sid:
    session['sid'] = f"ROOM-{token_hex(20)}"
  return render_template('chat.html', show_eruda=True,title="Webchat", session=session.get('sid', 'global')), 200

@view.route('/global/<name>')
def global_route(name):
  return render_template('chat.html', show_eruda=True, title="Global chat", session="global", name=name),200