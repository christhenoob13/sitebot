def Function(bot, event):
  data = {
    "body": "Kupal kaba boss?",
    "button": [
      dict(
        text = "Click",
        a = {
          "target": '_blank',
          "href": '/global'
        }
      ),
      dict(
        text = "Hello"
      )
    ]
  }
  bot.sendMessage(data)

config = {
  "name": 'test',
  "def": Function,
  "credits": 'Chriatopher'
}