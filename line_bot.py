from flask import Flask, request
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from crawler import WebScraper
from chatgpt import ChatGPT

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)
        access_token = ''
        secret = ''
        line_bot_api = LineBotApi(access_token)
        handler = WebhookHandler(secret)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        type = json_data['events'][0]['message']['type']
        if type == 'text':
            msg = json_data['events'][0]['message']['text']
            print(msg)
            if msg == '今日加密貨幣走勢':
                reply = get_crypto_analysis()
            elif msg == '今日新聞':
                reply = get_today_news()
        print(reply)
        line_bot_api.reply_message(tk, TextSendMessage(reply))
        body = request.get_data(as_text=True)
        json_data = json.loads(body)
        print(json_data)
    except:
        print(body)
    return 'OK'

def get_crypto_analysis():
    # 使用WebScraper爬取數據
    scraper = WebScraper()
    scraper.fetch_links_and_titles()
    json_data = scraper.to_json()
    
    # 使用ChatGPT分析數據
    chatgpt = ChatGPT()
    analysis = chatgpt.chat(json_data)
    
    return analysis.content

def get_today_news():
    # 使用WebScraper爬取數據
    scraper = WebScraper()
    scraper.fetch_links_and_titles()
    json_data = json.loads(scraper.to_json())
    
    # 格式化新聞資訊
    news_summary = "今日新聞摘要：\n\n"
    for item in json_data:
        news_summary += f"標題：\n{item['title']}\n"
        news_summary += f"概要：\n{item['content'][:100]}...\n"  # 只顯示前100個字符
        news_summary += f"連結：\n{item['url']}\n\n"
    
    return news_summary

if __name__ == "__main__":
    app.run()