import openai
import shared_variables

openai.api_key = shared_variables.gpt_token

chat_start = [
            {"role": "system", "content": "你是一个智能助手,请用中文回复我"}
        ]
chat_history = chat_start

def clear_chat_history():
    chat_history = chat_start

    
# generate gpt reply and add to chat_history
def generate_reply(message):
    # chat_history add user message
    chat_history.append({"role": "user", "content": message})

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = chat_history,
        )
    print(chat.choices[0].message.get('content'))
    # chat_history add assistant message
    chat_history.append({"role": "assistant", "content": chat.choices[0].message.get('content')})

    return chat.choices[0].message.get('content')
