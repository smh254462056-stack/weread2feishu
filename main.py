import os
import requests
import time

class WeRead2Feishu:
    def __init__(self):
        # 1. 自动读取 GitHub Secrets
        self.app_id = os.environ.get("FEISHU_APP_ID")
        self.app_secret = os.environ.get("FEISHU_APP_SECRET")
        self.app_token = os.environ.get("FEISHU_APP_TOKEN")
        
        # 2. 定位“慧敏的智库·悦读时光”物理 ID (已修正字符 l)
        self.table_id = "tbl8fl2VQpHdfPT7" 

    def get_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        res = requests.post(url, json=payload).json()
        return res.get("app_access_token")

    def run(self):
        token = self.get_token()
        if not token:
            print("❌ 获取 Token 失败，请检查 FEISHU_APP_ID 和 SECRET")
            return

        # 3. 构造写入地址 (Base 模式专用)
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 4. 数据封装 (严格匹配您的表头)
        payload = {
            "fields": {
                "书名": "🚀 智库系统·终极点火测试", 
                "状态": "同步成功",
                "笔记": "物理路径已重构，字符精度已对标。Base 模式链路正式贯通！",
                "阅读日期": int(time.time() * 1000)
            }
        }
        
        print(f"📡 正在尝试穿透物理路径... AppToken: {str(self.app_token)[:5]}***")
        res = requests.post(url, headers=headers, json=payload).json()
        
        if res.get("code") == 0:
            print("✨ [大功告成] 看到这条消息，说明您的智库已经成功联网！")
        else:
            print(f"⚠️ 报错码: {res.get('code')} | 错误信息: {res.get('msg')}")
            print(f"💡 高手提示: 如果还报 NOTEXIST，请检查 GitHub Secret 里的 APP_TOKEN 是否等于 MJ31b6FyKaPQRBsVjvHc4Qjbnkd")

if __name__ == "__main__":
    WeRead2Feishu().run()
