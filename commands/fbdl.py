from app.api_function import facebook_downloader

def fbdl(bot, data):
  if not data.args:
    return bot.sendMessage(":danger-color[:icon[fa-solid fa-warning]] Please provide facebook video link")
  if not data.args.startswith('https://') or 'facebook.com' not in data.args:
    return bot.sendMessage(":danger-color[:icon[fa-solid fa-warning]] Invalid link")
  loading = bot.sendMessage(f":icon[fa-solid fa-circle-notch fa-spin] Downloading facebook video")
  download = facebook_downloader(data.args)
  if 'error' in download:
    bot.unsendMessage(loading['id'])
    return bot.sendMessage(f":danger-color[:icon[fa-solid fa-warning]] {download['error']}")
  message = {
    "body": f":bold[:icon[fa-solid fa-clock] Duration: ] {download['duration']}",
    "attachment": {
      "src": download['videoHd'],
      "type": 'video'
    }
  }
  bot.unsendMessage(loading['id'])
  bot.sendMessage(message)
config = {
  "name": 'fbdl',
  "def": fbdl,
  "usage": "{p}fbdl <link>",
  "description": "Facebook video downloader",
  "credits": 'Greegmon'
}