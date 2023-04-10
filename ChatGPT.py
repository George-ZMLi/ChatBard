import openai


def GPT_req(user_input, apikey):
    openai.api_key = apikey
    organizationname = "Personal"
    organizationid = "org-IbbDYmOFQJzMayHUBHzjCvWS"

    model_engine = "text-davinci-003"

    config = {
        "model": "gpt3.5-turbo-0301",
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 0.9,
        "frequency_penalty": 0.1,
        "presence_penalty": 0.1
    }
    # model_engine = "gpt-3.5-turbo-0301"

    # 初始化对话上下文
    conversation_history = []

    # 将用户输入添加到对话上下文中
    conversation_history.append(user_input)
    # print("Your question:", conversation_history[-1])
    # 创建 OpenAI API 请求并将上一次生成结果添加到上下文中
    response = openai.Completion.create(
        engine=model_engine,
        prompt='\n'.join(conversation_history[-1]),
        max_tokens=config["max_tokens"],
        # n=1,
        # stop=None,
        # temperature=config["temperature"],
        # frequency_penalty=config["frequency_penalty"],
        # presence_penalty=config["presence_penalty"],
        # top_p=config["top_p"]
    )

    # 获取 GPT-3.5 生成的回复
    bot_reply = response.choices[0].text.strip()
    # print(response.choices)
    # bot_reply = response.choices[0].text
    # 将 GPT-3.5 生成的回复添加到对话上下文中
    conversation_history.append(bot_reply)

    return conversation_history[-1]


#
# Flag = 1
# # 开始对话循环
# while Flag:
#     # 提示用户输入对话内容
#     user_input = input("You: ")
#
#     # String = "你好，我叫George，你叫什么名字？"
#     print("You said: ", user_input)
#     response = GPT_req(user_input)
#     print("Bot: " + response)
#     print(type(response))
#     print('---------------------------------')
#     if "bye" or "Bye" in user_input:
#         Flag = 0
#         break
#
