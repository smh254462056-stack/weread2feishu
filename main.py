import os
import requests
import json
import time

class WeRead2Feishu:
    def __init__(self):
        # 1. 自动从 GitHub Secrets 读取密钥
        self.cookie = os.environ.get("WEREAD_COOKIE")
        self.app_id = os.environ.get("FEISHU_APP_ID")
        self.app_secret = os.environ.get("FEISHU_APP_SECRET")
        self.app_token = os.environ.get("FEISHU_APP_TOKEN")
        
        # 2. 您的物理 Table ID
        self.table_id = "tblmH78Bv3p9W5kR" 

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
        """同步执行引擎"""
        token = self.get_feishu_token()
        if not token:
            return

        # 3. 构造飞书多维表格写入地址
        write_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8"
        }
        
        # 4. 构造写入载荷 (确保飞书表头包含“书名”字段)
        payload = {
            "fields": {
                "书名": "✅ 自动化同步物理测试成功",
                "状态": "已同步"
            }
        }
        
        print(f"🚀 启动生产同步引擎，目标表: {self.table_id}...") 
        
        try:
            # 5. 执行真实的物理写入动作
            response = requests.post(write_url, headers=headers, json=payload)
            result = response.json()
            
            if result.get("code") == 0:
                print("✨ [核心资产搬运成功] 飞书已接收数据！")
            else:
                print(f"⚠️ 飞书响应异常: {result.get('msg')}")
                print(f"💡 排障提示: 请检查机器人是否已加入该多维表格。")
        except Exception as e:
            print(f"❌ 写入发生致命错误: {e}")

if __name__ == "__main__":
    worker = WeRead2Feishu()
    worker.run()
