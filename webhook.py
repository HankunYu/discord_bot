import requests
import json
import discord
import discord_bot
import asyncio
from shared_variables import current_channel
from urllib.parse import quote

"""
movie pilot webhook
解析并处理命令
"""
access_token = None
def send_message(data, action):
    global access_token
    if(access_token == None):
        login()
    webhook_url = 'http://192.168.50.11:4001/api/v1'

    # 处理订阅====================
    if(action == 'subscribe'):
        webhook_url += '/subscribe/'

        get_headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
        print(access_token)
        response = requests.get(webhook_url, headers=get_headers)
        
        if response.status_code == 200 or response.status_code == 204:  
            print('消息已发送成功')
        else:
            print(response.status_code)
            print('测试消息失败')
        # print(response.text)
    # 处理搜索====================
    elif(action == 'search'):
        webhook_url += '/media/search'
        quoted_data = quote(data)
        request_url = '?title=' + quoted_data + '&page=1&count=8'
        webhook_url += request_url
        get_headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.get(webhook_url, headers=get_headers)
        
        loop = asyncio.get_event_loop()
        try:
            json_data = response.json()
        except:
            json_data = []
            print('返回数据不是json格式')
            asyncio.run_coroutine_threadsafe(discord_bot.send_message('搜索: ' + data + ' 没有找到有用信息'), loop)
            return None
            
        # 发送消息
        for movie in json_data:
            embad = discord.Embed(
                title= movie.get('type') + ' '+ movie.get('title'), 
                description=movie.get('detail_link') + '\n' + movie.get('overview'), 
                color=0xeee657)
            embad.set_image(url=movie.get('poster_path'))
            button = discord.ui.Button(label='订阅', style=discord.ButtonStyle.green,custom_id="my_button")
            button.callback =  asyncio.run(subscribe(),loop)
            view = discord.ui.View()
            view.add_item(button)
            asyncio.run_coroutine_threadsafe(discord_bot.send_message(None,embad,view), loop)

        if response.status_code == 200 or response.status_code == 204:  
            print('消息已发送成功' + response.text)
        else:
            print(response.status_code)
            print('测试消息失败')
            asyncio.run_coroutine_threadsafe(discord_bot.send_message('后端有点问题，没有获取到正确信息'), loop)
    # 处理下载====================
    elif(action == 'download'):
        webhook_url += '/search/media/tmdb?3A'
        request_url = data
        webhook_url += request_url
        get_headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + access_token
        }
        response = requests.get(webhook_url, headers=get_headers)
        try:
            json_data = response.json()
        except:
            json_data = []
            print('返回数据不是json格式')
            asyncio.run_coroutine_threadsafe(discord_bot.send_message('搜索下载资源: ' + data + ' 没有找到有用信息'), loop)
            return None
        
        # format data
        for media in json_data:
            embad = discord.Embed(
                title= media.get('type') + ' '+ media.get('title'), 
                description=media.get('detail_link') + '\n' + media.get('overview'), 
                color=0xeee657)
            embad.set_image(url=media.get('poster_path'))
            button = discord.ui.Button(label='下载', style=discord.ButtonStyle.green)
            button.callback = subscribe()
            view = discord.ui.View()
            view.add_item(button)
            asyncio.run_coroutine_threadsafe(discord_bot.send_message(None,embad,view), loop)

async def subscribe():
    # global access_token
    # if(access_token == None):
    #     login()
    # webhook_url = 'http://192.168.50.11:4001/api/v1'
    # await interaction.response.send_message("按钮被点击！")
    print('movie_id')


def login():
    global access_token
    global session
    url = 'http://192.168.50.11:4001/api/v1/login/access-token'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': '',
        'username': 'Hankun',
        'password': 'yu759520',
        'scope': '',
        'client_id': 'webhook',
        'client_secret': 'webhook'
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        json_data = response.json()
        access_token = json_data['access_token']
        print('登录成功')
    else:
        print('登录失败') 


# 测试
if __name__ == '__main__':

    data = '你的名字'
    send_message(data, 'search')
    # login()