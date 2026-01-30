import os
import requests
import time

class WeRead2Feishu:
    def __init__(self):
        # 强制清除变量名可能的干扰
        self.app_id = os.environ.get("FEISHU_APP_ID", "").strip()
        self.app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
        self.app_token = os.environ.get("FEISHU_APP_TOKEN", "").strip()
        
        # 100% 物理对标 ID
        self.table_id = "tbl8fl2VQpHdfPT7" 

    def get_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        try:
            res = requests.post(url, json=payload, timeout=10).json()
            return res.get("app_access_token")
        except:
            return None

    def run(self):
        token = self.get_token()
        if not token:
            print(f"❌ 授权失败！请检查 GitHub Secrets 中的 ID 和 SECRET 是否正确填入。")
            return

        if not self.app_token:
            print(f"❌ 致命错误：读取不到 FEISHU_APP_TOKEN。请检查 GitHub Secrets 变量名是否完全一致。")
            return

        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        payload = {
            "fields": {
                "书名": "🚀 终极点火·物理贯通测试", 
                "状态": "同步成功",
                "笔记": "环境变量已对标，物理路径已闭环。",
                "阅读日期": int(time.time() * 1000)
            }
        }
        
        print(f"📡 穿透测试开始... 目标大楼: {self.app_token[:5]}***")
        res = requests.post(url, headers=headers, json=payload).json()
        
        if res.get("code") == 0:
            print("✨ [大功告成] 您的智库已正式连接互联网！")
        else:
            print(f"⚠️ 写入受阻: {res.get('msg')} (代码: {res.get('code')})")

if __name__ == "__main__":
    WeRead2Feishu().run()
