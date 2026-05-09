import time
import json
import urllib.request
import urllib.parse
from apscheduler.schedulers.background import BackgroundScheduler

# 你的配置（已经帮你填好了）
BARK_KEY = "FNHsHZzGM2sirZcncfkgbb"
ROCOM_API_KEY = "sk-ff14f964051a5c966564e29b5bd3a768"
MERCHANT_API_URL = "https://api.rocom.cn/api/v1/public/yuancheng"

def send_bark(title, content):
    encoded_title = urllib.parse.quote(title)
    encoded_content = urllib.parse.quote(content)
    url = f"https://api.day.app/{BARK_KEY}/{encoded_title}/{encoded_content}?sound=birds.caf&group=远行商人"
    try:
        urllib.request.urlopen(url, timeout=10)
        print("✅ 推送成功")
    except Exception as e:
        print(f"❌ 推送失败：{e}")

def run_push_task():
    print("🔍 正在拉取远行商人数据...")
    try:
        headers = {"Authorization": f"Bearer {ROCOM_API_KEY}"}
        req = urllib.request.Request(MERCHANT_API_URL, headers=headers, method="GET")
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = response.read().decode("utf-8")
            data = json.loads(res_data)
        
        if data.get("code") == 200:
            info = data["data"]
            title = "🛒 远行商人提醒"
            content = f"⏰ 刷新时间：{info['refreshTime']}\n🌍 星球：{info['planet']}\n🎁 商品：{info['goods']}"
            send_bark(title, content)
        else:
            send_bark("⚠️ 商人提醒", f"API返回异常：{data.get('message', '未知错误')}")
    except Exception as e:
        send_bark("❌ 商人提醒", f"任务错误：{str(e)}")

# 启动定时任务（每天08:00/12:00/16:00/20:00运行）
if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_push_task, 'cron', hour='8,12,16,20')
    scheduler.start()
    print("✅ 定时任务已启动，等待运行...")
    while True:
        time.sleep(60)
