# Sitebot <small>v2</small>
Sitebot is a website bot, by typing various commands you can interact with this bot

## Whats new?
- Clickable button
  <details>
    <summary>Show example</summary>

    ```py
    bot.sendMessage({
      "body": "Example Message",
      "button": {
        "text": "Click Me!",
        "a": {
          "href": 'https://google.com',
          "target": '_blank'
        },
        "style": {} # custon css style
      }
    })
    ```
  </details>