from openai import OpenAI
import json

class ChatGPT:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model
        self.client = OpenAI(
            api_key=''
        )

    def chat(self, json_data):
        data = json.loads(json_data)
        message = "以下是今日的加密貨幣新聞：\n\n"
        for item in data:
            message += f"標題：{item['title']}\n內容：{item['content']}\n\n"
        
        message += "請分析這些新聞，並總結今日加密貨幣市場的走勢。"

        msgs = [
            {"role": "system", "content": "#zh-TW 你是一個專業的加密貨幣分析師，請根據提供的新聞分析今日加密貨幣市場走勢。"},
            {"role": "system", "content": "#zh-TW Use Traditional Chinese language only"},
            {"role": "system", "content": "#zh-TW Use Traditional Chinese alphabet whenever possible"},
            {"role": "system", "content": "#zh-TW Do not use English except in programming languages if any"},
            {"role": "system", "content": "#zh-TW Avoid the Latin alphabet whenever possible"},
            {"role": "system", "content": "#zh-TW Translate any other language to the Traditional Chinese language whenever possible"},
            {"role": "user", "content": message},
        ]

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=msgs
        )
        return completion.choices[0].message



