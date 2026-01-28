import os
import requests
import json
import time
from datetime import datetime

class WeRead2Feishu:
    def __init__(self):
        # 1. 自动从 GitHub Secrets 读取密钥
        self.cookie = os.environ.get("WEREAD_COOKIE")
        self.app_id = os.environ.get("FEISHU_APP_ID")
        self.app_secret = os.environ.get("FEISHU_APP_SECRET")
        self.app_token = os.environ.get("FEISHU_APP_TOKEN")
        
        # 2. 定位“慧敏-个人图书馆”的真实物理 ID
        self.table_id = "tblYVQUs42AcNa3C" 

    def get_feishu_token(self):
        """获取飞书授权令牌"""
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        try:
            res = requests.post(url, json=payload)
            res_data = res.json()
            if res_data.get("code") != 0:
                print(f"❌ 获取 Token 失败: {res_data.get('msg')}")
                return None
            return res_data.get("app_access_token")
        except Exception as e:
            print(f"❌ 网络请求异常: {e}")
            return None

    def run(self):
        """同步执行主逻辑"""
        token = self.get_feishu_token()
        if not token:
            return

        # 3. 构造写入地址
        write_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 4. 四维度数据封装 (匹配您的最新表头：书名、状态、笔记、阅读日期)
        payload = {
            "fields": {
                "书名": "✅ 慧敏的自动化系统点火测试", 
                "状态": "同步成功",
                "笔记": "恭喜！当您看到这行字，说明从 GitHub 到您个人飞书的链路已彻底打通。",
                "阅读日期": int(time.time() * 1000) 
            }
        }
        
        print(f"🚀 正在向新表写入数据... 目标 Table ID: {self.table_id}") 
        
        try:
            response = requests.post(write_url, headers=headers, json=payload)
            result = response.json()
            
            if result.get("code") == 0:
                print("✨ [大功告成] 数据已成功同步至“慧敏-个人图书馆”！")
            else:
                print(f"⚠️ 写入失败: {result.get('msg')}")
                print(f"💡 检查建议：确保您的飞书应用已加入该表，且 Secrets 中的 App Token 已更新为 UnKY...Bg")
        except Exception as e:
            print(f"❌ 运行发生异常: {e}")

if __name__ == "__main__":
    worker = WeRead2Feishu()
    worker.run()
