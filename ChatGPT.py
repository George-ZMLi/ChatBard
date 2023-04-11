import openai

class GPT:
    def __init__(self, apikey):
        self.apikey = apikey
        self.history = []
        openai.api_key = apikey

    def GPT_req(self, user_input):
        model_engine = "text-davinci-003"

        config = {
            "model": "gpt3.5-turbo-0301",
            "temperature": 0.7,
            "max_tokens": 1024,
            "top_p": 0.9,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1
        }

        # 将用户输入添加到对话上下文中
        self.history.append(user_input)
        # 创建 OpenAI API 请求并将上一次生成结果添加到上下文中
        response = openai.Completion.create(
            engine=model_engine,
            prompt='\n'.join(self.history[-1]),
            max_tokens=config["max_tokens"],
            # n=1,
            # stop=None,
            # temperature=config["temperature"],
            # frequency_penalty=config["frequency_penalty"],
            # presence_penalty=config["presence_penalty"],
            # top_p=config["top_p"]
        )

        bot_reply = response.choices[0].text.strip()
        self.history.append(bot_reply)

        return self.history[-1]


