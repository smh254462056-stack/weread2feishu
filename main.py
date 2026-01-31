import os
import requests
import time

class WeRead2Feishu:
    def __init__(self):
        # 从环境变量读取配置（匹配 GitHub Secrets 中的变量名）
        self.app_id = os.environ.get("FEISHU_APP_ID", "").strip()
        self.app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
        self.app_token = os.environ.get("TABLE_ID", "").strip()  # 对应你填的 Base ID
        
        # 从环境变量读取 Table ID（建议新增一个 SECRET：FEISHU_TABLE_ID）
        # 如果你暂时不想新增，也可以直接替换成正确的 Table ID
        self.table_id = os.environ.get("FEISHU_TABLE_ID", "tbl8f12VQpHdfPT7").strip()

    def get_token(self):
        """获取飞书应用访问令牌"""
        url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        payload = {"app_id": self.app_id, "app_secret": self.app_secret}
        try:
            res = requests.post(url, json=payload, timeout=10).json()
            if res.get("code") != 0:
                print(f"❌ 获取 Token 失败：{res.get('msg')}")
                return None
            return res.get("app_access_token")
        except Exception as e:
            print(f"❌ 网络请求异常：{str(e)}")
            return None

    def run(self):
        """核心运行逻辑"""
        # 1. 校验基础配置
        if not all([self.app_id, self.app_secret, self.app_token, self.table_id]):
            print(f"❌ 配置不完整！请检查以下变量：")
            print(f"   - FEISHU_APP_ID: {'✅' if self.app_id else '❌'}")
            print(f"   - FEISHU_APP_SECRET: {'✅' if self.app_secret else '❌'}")
            print(f"   - TABLE_ID (Base ID): {'✅' if self.app_token else '❌'}")
            print(f"   - FEISHU_TABLE_ID (Table ID): {'✅' if self.table_id else '❌'}")
            return
        
        # 2. 获取访问令牌
        token = self.get_token()
        if not token:
            return

        # 3. 构造请求
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
        
        # 4. 发送请求
        print(f"📡 开始写入数据... Base ID: {self.app_token[:5]}***, Table ID: {self.table_id[:5]}***")
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=15).json()
            
            if res.get("code") == 0:
                print("✨ [大功告成] 数据已成功写入飞书多维表格！")
                print(f"   记录 ID: {res.get('data', {}).get('record', {}).get('record_id')}")
            else:
                print(f"⚠️ 写入失败: {res.get('msg')} (错误码: {res.get('code')})")
                # 常见错误提示
                if res.get('code') == 1254041:
                    print("   ❗ 可能原因：Table ID/Base ID 错误、应用无表格访问权限")
        except Exception as e:
            print(f"❌ 请求异常：{str(e)}")

if __name__ == "__main__":
    WeRead2Feishu().run()
