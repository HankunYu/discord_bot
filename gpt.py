import openai
import json
import webhook
import discord_bot

openai.api_key = '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'
chat_history = [
            {"role": "system", "content": "你是一个智能助手,请用中文回复我"}
        ]
chat_start = [
            {"role": "system", "content": "你是一个智能助手,请用中文回复我"}
        ]

def clear_chat_history():
    chat_history = chat_start

# 识别用户的意图
def define_command(message):
    propose = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "分析我发你的内容,当识别到我有下载/订阅/搜索电影或者电视剧的意向时候回复action,其余情况回复chat"},
            {"role": "user", "content": "我想看霸王别姬"},
            {"role": "assistant", "content": "action"},
            {"role": "user", "content": "我好无聊"},
            {"role": "assistant", "content": "chat"},
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": "chat"},
            {"role": "user", "content": message}
        ]
        )
    answer = propose.choices[0].message.get('content')
    if(answer == 'action'):
        return run_command(message)
    else:
        return generate_reply(message)
    
# 生成回复,并添加到chat_history
def generate_reply(message):
    # chat_history 添加用户输入
    chat_history.append({"role": "user", "content": message})

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = chat_history,
        )
    print(chat.choices[0].message.get('content'))
    # chat_history 添加助手回复
    chat_history.append({"role": "assistant", "content": chat.choices[0].message.get('content')})

    return chat.choices[0].message.get('content')

# 识别为命令则执行webhook
def run_command(command):
        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "请帮我分析我发你的内容,如果可以识别就以json格式回复我: '{'action: title: '}',action的行为只有subscribe,download,search, 如果不能识别请回复我抱歉并询问详细内容,电影两个字不能作为title"},
            {"role": "user", "content": command}
        ]
        )
        reply = completion.choices[0].message.get('content')
        print(reply)
        if reply.startswith('抱歉'):
            return reply
        try:
            reply = json.loads(reply)
        except:
            return reply + ' 不是json'
        webhook.send_message(reply.get('title'), reply.get('action'))