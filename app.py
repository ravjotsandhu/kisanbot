import asyncio
from cgitb import text
from os import stat
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from bs4 import BeautifulSoup
import requests


async def handle(msg):
    global chat_id
    global state, city, crop
    # These are some useful variables
    content_type, chat_type, chat_id = telepot.glance(msg)
    # Log variables
    print(content_type, chat_type, chat_id)
    text = msg['text'].split(' ')
    print(text)
    command = text[0]
    username = msg['chat']['first_name']
    # Check that the content type is text and not the starting
    if content_type == 'text':
        if command == '/start':
            await bot.sendMessage(chat_id, 'enter name of state city to get rates via /state, /city, /crop commands')
            # await bot.getUpdates()
        if command == '/state':
            state = text[1]
            # await bot.sendMessage(chat_id, 'enter name of state')
            # await bot.getUpdates()
        if command == '/city':
            city = text[1]
            # await bot.sendMessage(chat_id, 'enter name of city')
            # await bot.getUpdates()
        if command == '/crop':
            crop = text[1]

            # await bot.sendMessage(chat_id, 'rates found!')
        if command == '/getrates':
            await getrates(state+'/'+city+'/'+crop)
        if command == '/weather':
            await weather(state+'/'+city)


async def getrates(params):
    # create url
    url = 'https://agriplus.in/mandi/' + params
    # define headers
    headers = {'User-Agent': 'Generic user agent'}
    # get page
    page = requests.get(url, headers=headers)
    # let's soup the page
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup)
    try:
        try:
            # get definition
            title = soup.find(
                'thead', {'th': ''}).text
            print(title)
            rates = soup.find(
                'tbody', {'tr': ''}).text
            print(rates)
            data = title+'\n'+rates
            # send message
            await bot.sendMessage(chat_id, data)
        except:
            await bot.sendMessage(chat_id, 'rates not found!')
    except:
        await bot.sendMessage(chat_id, 'Something went wrong...')


async def weather(params):
    # create url
    url = 'https://www.theweathernetwork.com/in/weather/' + params
    # define headers
    headers = {'User-Agent': 'Generic user agent'}
    # get page
    page = requests.get(url, headers=headers)
    # let's soup the page
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup)
    try:
        try:
            # get definition
            data = soup.find(
                'div', attrs={'class': 'obs-area'}).text
            print(data)
            # send message
            await bot.sendMessage(chat_id, data)
        except:
            await bot.sendMessage(chat_id, 'forecast not found!')
    except:
        await bot.sendMessage(chat_id, 'Something went wrong...')


# Program startup
TOKEN = 'api token'
bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, handle).run_forever())
print('Listening ...')

# Keep the program running
loop.run_forever()
'''
import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
from bs4 import BeautifulSoup
import requests


async def handle(msg):
    global chat_id
    # These are some useful variables
    content_type, chat_type, chat_id = telepot.glance(msg)
    # Log variables
    print(content_type, chat_type, chat_id)
    print(msg)
    username = msg['chat']['first_name']
    # Check that the content type is text and not the starting
    if content_type == 'text':
        if msg['text'] != '/start':
            text = msg['text']
            # it's better to strip and lower the input
            text = text.strip()
            await getrates(text.lower())


async def getrates(text):
    # create url
    url = 'https://agriplus.in/mandi/haryana/shahbad/' + text
    # define headers
    headers = {'User-Agent': 'Generic user agent'}
    # get page
    page = requests.get(url, headers=headers)
    # let's soup the page
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup)
    try:
        try:
            # get definition
            title = soup.find(
                'thead', {'th': ''}).text
            print(title)
            rates = soup.find(
                'tbody', {'tr': ''}).text
            print(rates)
            data = title+'\n'+rates
            # send message
            await bot.sendMessage(chat_id, data)
        except:
            await bot.sendMessage(chat_id, 'rates not found!')
    except:
        await bot.sendMessage(chat_id, 'Something went wrong...')

# Program startup
TOKEN = 'api token'
bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, handle).run_forever())
print('Listening ...')

# Keep the program running
loop.run_forever()
'''
