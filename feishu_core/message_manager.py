"""
飞书消息管理模块
"""
import requests
import json
from typing import List, Dict, Any, Optional, Union


class MessageManager:
    """消息管理器"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        初始化消息管理器
        
        Args:
            app_id: 飞书应用ID
            app_secret: 飞书应用密钥
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.base_url = "https://open.feishu.cn/open-apis"
        self.tenant_access_token = None
    
    def _get_access_token(self) -> str:
        """获取租户访问令牌"""
        if self.tenant_access_token:
            return self.tenant_access_token
        
        url = f"{self.base_url}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if result.get("code") == 0:
            self.tenant_access_token = result.get("tenant_access_token")
            return self.tenant_access_token
        else:
            raise Exception(f"获取访问令牌失败: {result.get('msg')}")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }
    
    def send_text_message(self, receive_id: str, content: str, 
                         receive_id_type: str = "open_id") -> str:
        """
        发送文本消息
        
        Args:
            receive_id: 接收者ID
            content: 消息内容
            receive_id_type: 接收者ID类型（open_id/user_id/union_id/chat_id）
            
        Returns:
            消息ID
        """
        url = f"{self.base_url}/im/v1/messages"
        data = {
            "receive_id": receive_id,
            "receive_id_type": receive_id_type,
            "msg_type": "text",
            "content": json.dumps({"text": content})
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("message_id")
        else:
            raise Exception(f"发送文本消息失败: {result.get('msg')}")
    
    def send_card_message(self, receive_id: str, card_content: Dict[str, Any],
                         receive_id_type: str = "open_id") -> str:
        """
        发送卡片消息
        
        Args:
            receive_id: 接收者ID
            card_content: 卡片内容
            receive_id_type: 接收者ID类型
            
        Returns:
            消息ID
        """
        url = f"{self.base_url}/im/v1/messages"
        data = {
            "receive_id": receive_id,
            "receive_id_type": receive_id_type,
            "msg_type": "interactive",
            "content": json.dumps(card_content)
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("message_id")
        else:
            raise Exception(f"发送卡片消息失败: {result.get('msg')}")
    
    def send_image_message(self, receive_id: str, image_key: str,
                          receive_id_type: str = "open_id") -> str:
        """
        发送图片消息
        
        Args:
            receive_id: 接收者ID
            image_key: 图片key
            receive_id_type: 接收者ID类型
            
        Returns:
            消息ID
        """
        url = f"{self.base_url}/im/v1/messages"
        data = {
            "receive_id": receive_id,
            "receive_id_type": receive_id_type,
            "msg_type": "image",
            "content": json.dumps({"image_key": image_key})
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("message_id")
        else:
            raise Exception(f"发送图片消息失败: {result.get('msg')}")
    
    def send_file_message(self, receive_id: str, file_key: str,
                         receive_id_type: str = "open_id") -> str:
        """
        发送文件消息
        
        Args:
            receive_id: 接收者ID
            file_key: 文件key
            receive_id_type: 接收者ID类型
            
        Returns:
            消息ID
        """
        url = f"{self.base_url}/im/v1/messages"
        data = {
            "receive_id": receive_id,
            "receive_id_type": receive_id_type,
            "msg_type": "file",
            "content": json.dumps({"file_key": file_key})
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("message_id")
        else:
            raise Exception(f"发送文件消息失败: {result.get('msg')}")
    
    def reply_message(self, message_id: str, content: str, 
                     reply_in_thread: bool = False) -> str:
        """
        回复消息
        
        Args:
            message_id: 被回复的消息ID
            content: 回复内容
            reply_in_thread: 是否在话题中回复
            
        Returns:
            消息ID
        """
        url = f"{self.base_url}/im/v1/messages"
        
        data = {
            "reply_in_thread": reply_in_thread
        }
        
        # 根据回复内容类型设置消息类型
        if isinstance(content, dict):
            # 卡片消息
            data["msg_type"] = "interactive"
            data["content"] = json.dumps(content)
        elif content.startswith("http"):
            # 图片消息
            data["msg_type"] = "image"
            data["content"] = json.dumps({"image_key": content})
        else:
            # 文本消息
            data["msg_type"] = "text"
            data["content"] = json.dumps({"text": content})
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("message_id")
        else:
            raise Exception(f"回复消息失败: {result.get('msg')}")
    
    def get_message(self, message_id: str) -> Dict[str, Any]:
        """
        获取消息详情
        
        Args:
            message_id: 消息ID
            
        Returns:
            消息详情
        """
        url = f"{self.base_url}/im/v1/messages/{message_id}"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取消息详情失败: {result.get('msg')}")
    
    def get_chat_history(self, container_id: str, container_type: str = "chat",
                        start_time: str = None, end_time: str = None,
                        page_size: int = 50, page_token: str = None) -> Dict[str, Any]:
        """
        获取聊天记录
        
        Args:
            container_id: 容器ID（如群聊ID）
            container_type: 容器类型（chat/p2p）
            start_time: 开始时间
            end_time: 结束时间
            page_size: 每页数量
            page_token: 分页令牌
            
        Returns:
            聊天记录
        """
        url = f"{self.base_url}/im/v1/messages"
        params = {
            "container_id": container_id,
            "container_id_type": container_type,
            "page_size": page_size
        }
        
        if start_time:
            params["start_time"] = start_time
        if end_time:
            params["end_time"] = end_time
        if page_token:
            params["page_token"] = page_token
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取聊天记录失败: {result.get('msg')}")
    
    def delete_message(self, message_id: str) -> bool:
        """
        删除消息
        
        Args:
            message_id: 消息ID
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/im/v1/messages/{message_id}"
        response = requests.delete(url, headers=self._get_headers())
        result = response.json()
        
        return result.get("code") == 0
    
    def recall_message(self, message_id: str) -> bool:
        """
        撤回消息
        
        Args:
            message_id: 消息ID
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/im/v1/messages/{message_id}"
        data = {"msg_type": "text"}  # 任意消息类型
        
        response = requests.patch(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        return result.get("code") == 0
    
    def send_rich_text_message(self, receive_id: str, title: str,
                               content: List[Dict[str, Any]],
                               receive_id_type: str = "open_id") -> str:
        """
        发送富文本消息
        
        Args:
            receive_id: 接收者ID
            title: 富文本标题
            content: 富文本内容
            receive_id_type: 接收者ID类型
            
        Returns:
            消息ID
        """
        url = f"{self.base_url}/im/v1/messages"
        data = {
            "receive_id": receive_id,
            "receive_id_type": receive_id_type,
            "msg_type": "post",
            "content": json.dumps({
                "post": {
                    "zh_cn": {
                        "title": title,
                        "content": content
                    }
                }
            })
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("message_id")
        else:
            raise Exception(f"发送富文本消息失败: {result.get('msg')}")
    
    def create_notification_card(self, title: str, content: str,
                                 buttons: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        创建通知卡片
        
        Args:
            title: 卡片标题
            content: 卡片内容
            buttons: 按钮列表
            
        Returns:
            卡片内容
        """
        card = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "title": {
                    "content": title,
                    "tag": "plain_text"
                }
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "content": content,
                        "tag": "lark_md"
                    }
                }
            ]
        }
        
        if buttons:
            for button in buttons:
                card["elements"].append({
                    "tag": "action",
                    "actions": [
                        {
                            "tag": "button",
                            "text": {
                                "content": button.get("text", ""),
                                "tag": "plain_text"
                            },
                            "url": button.get("url", ""),
                            "type": "primary"
                        }
                    ]
                })
        
        return card
    
    def send_notification(self, receive_id: str, title: str, content: str,
                        buttons: List[Dict[str, str]] = None,
                        receive_id_type: str = "open_id") -> str:
        """
        发送通知消息
        
        Args:
            receive_id: 接收者ID
            title: 通知标题
            content: 通知内容
            buttons: 按钮列表
            receive_id_type: 接收者ID类型
            
        Returns:
            消息ID
        """
        card_content = self.create_notification_card(title, content, buttons)
        return self.send_card_message(receive_id, card_content, receive_id_type)
