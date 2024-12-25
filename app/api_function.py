from bs4 import BeautifulSoup
import requests
import os
import json
import random
import re
import base64

userAgent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"

# imgbb upload
def imgbb(data):
  KEY = os.getenv('IMGBB_KEY')
  base_url = "https://api.imgbb.com/1/upload"
  params = {
    "name": 'sitebot',
    "key": KEY,
    "expiration": 1512000 # 25 weeks, remove this to set no expiration
  }
  data = {"image": data}
  try:
    res = requests.post(base_url,
      params=params,
      data=data,
      timeout=10
    )
    img = res.json()
    if img.get('success'):
      return {
        "image": img["data"]["url"],
        "width": img["data"]["width"],
        "height": img["data"]["height"]
      }
    return {
      "error": img["error"]["message"]
    }
  except Exception as e:
    print("ERROR: ", e)
    return {"error": 'Server error'}

# Website screenshot
def website_screenshot(link):
  pattern = re.compile(r'https?://[^\s]+')
  try:
    match = pattern.search(link)
    if match:
      res = requests.get('https://urltoscreenshot.com/',headers={"User-Agent":userAgent})
      soup = BeautifulSoup(res.content, 'html.parser')
      m1 = soup.find_all('script')
      m2 = m1.pop().get_text()
      KEY = m2.split("x-api-key', '")[1].split("'")[0]
      url = 'https://api.apilight.com/screenshot/get'
      data = {
        'url': match.group(),
        'base64': '1',
        'width': 1366,
        'height': 1024
      }
      header = {'x-api-key':KEY,"User-Agent":userAgent}
      response = requests.get(url, headers=header, params=data).text
      base64_image = response
      litrato = imgbb(base64_image)
      return litrato
    else:
      return {"error": "Invalid website link"}
  except Exception as e:
    print("ERROR: ", e)
    return {"error": "An error accured while taking an screenshot"}

# Tiktok video downloader
def tiktok_downloader(link: str) -> dict:
  try:
    url = "https://ttsave.app/download"
    headers = {
      "Content-Type": 'application/json',
      "User-Agent": userAgent,
      "Accept": "application/json, text/plain, */*"
    }
    data = {"query": link,"languange_id": "1"}
    
    res = requests.post(url,
      json=data,
      headers=headers,
      timeout=10
    )
    html = BeautifulSoup(res.content, 'html.parser')
    
    buttons = html.find('div', id='button-download-ready')
    mdiv = html.find('div', class_="flex flex-row items-center justify-center gap-1 mt-5 w-3/4")
    row = html.find('div',class_="flex flex-row items-center justify-center gap-2 mt-2")
    
    if html.text == 'Error unknown':
      return {"error": "Error while proccessing the data"}
    cols = row.find_all('div',class_='flex-row')
    
    username = html.find('a', class_="font-extrabold text-blue-400 text-xl mb-2").text
    description = html.find('p', class_="text-gray-600 px-2 text-center break-all w-3/4 oneliner").text or 'No description'
    views = cols[0].text.strip() or '0'
    comments = cols[2].text.strip() or '0'
    shares = cols[4].text.strip() or '0'
    music = mdiv.find('span', class_="text-gray-500").text or 'unknown'
    videoLink = html.find('a', attrs={'type':"no-watermark"}).get('href')
    data = {
      "username": username,
      "description": description,
      "views": views,
      "comments": comments,
      "shares": shares,
      "music": music,
      "videoSource": videoLink
    }
    return data
  except Exception as e:
    print("ERROR: ", e)
    return {"error": f"Error while fetching the data."}

# Shoti
def shoti() -> dict:
  shoti_json = json.load(open('commands/cache/shoti.json', 'r'))
  shoti_list = shoti_json['link']
  random_link = random.choice(shoti_list)
  data = tiktok_downloader(random_link)
  return data

# bible verse
def random_bible_verse():
  try:
    url = "https://dailyverses.net/random-bible-verse"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    content = soup.find('div',class_='content')
    b1 = content.find('div',class_='b1')
    
    text = b1.find('span',class_='v1').getText()
    verse = b1.find('a',class_='vc').getText()
    
    return {"text": text, "verse": verse}
  except Exception as e:
    print("ERROR: ", e)
    return {"error": f"{e}"}

# Paster
def paster(paste):
  try:
    session = requests.Session()
    url = "https://pastebin.mozilla.org";
    
    headers = {
      "Content-Type": 'application/x-www-form-urlencoded',
      "User-Agent": userAgent,
      "Referer": url
    }
    data = {}
    
    res = session.get(url).content
    soup = BeautifulSoup(res, 'html.parser')
    form = soup.find('form')
    token = form.find('input', attrs={"name":"csrfmiddlewaretoken"}).get('value')
    
    data["csrfmiddlewaretoken"] = token
    data["title"] = ''
    data["lexer"] = '_text'
    data["expires"] = 86400
    data["content"] = paste
    
    response = session.post(url, data=data, headers=headers)
    resHtml = BeautifulSoup(response.content, 'html.parser')
    
    ul = resHtml.find('ul',id="snippetOptions")
    resTitle = resHtml.find('title').getText()
    
    expire = ul.find('li',class_='option-type').getText().split('in: ')[1].strip()
    path = resTitle.split('Pastebin')[1].split(' ')[0]
    text = ul.find("textarea", id="copySnippetSource").getText()
    return {
      "path": '/paster' + path,
      "text": text,
      "expire": ' '.join(expire.split('\xa0'))
    }
  except Exception as e:
    print("Exception: ", e)
    return {"error": f"{e}"}

# facebook video/reel downloader
def facebook_downloader(link):
  if not link:
    return {"error":"Missing facebook video link"}
  if 'facebook.com' not in link:
    return {"error":"Invalid link"}
  try:
    url = "https://fdown.net/download.php"
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36"}
    data = {
      "URLz": link
    }
    res = requests.post(url, data=data, headers=headers)
    html = res.content
    
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find('div', class_="row box-shadow")
    deck = data.find_all('div', class_='lib-row')[-1]
    
    thumbnail = data.find('img').get('data-cfsrc','src').replace('&amp;','&')
    videoNormal = soup.find("a",id="sdlink").get('href')
    videoHd = soup.find("a",id="hdlink").get('href')
    duration = deck.get_text().split("Duration:")[1].strip()
    return {
      "thumbnail": thumbnail,
      "videoNormal": videoNormal,
      "videoHd": videoHd,
      "duration": duration
    }
  except Exception as e:
    print("ERROR: ", e)
    return {"error": "An error accured while fetching the data, please make sure that the url is facebook link"}