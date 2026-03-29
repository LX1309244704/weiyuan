"""
飞书日历管理模块
"""
import requests
import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class CalendarManager:
    """日历管理器"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        初始化日历管理器
        
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
    
    def get_primary_calendar(self) -> Dict[str, Any]:
        """
        获取主日历
        
        Returns:
            主日历信息
        """
        url = f"{self.base_url}/calendar/v4/calendars/primary"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取主日历失败: {result.get('msg')}")
    
    def list_calendars(self) -> List[Dict[str, Any]]:
        """
        列出所有日历
        
        Returns:
            日历列表
        """
        url = f"{self.base_url}/calendar/v4/calendars"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("calendar_list", [])
        else:
            raise Exception(f"获取日历列表失败: {result.get('msg')}")
    
    def get_calendar(self, calendar_id: str) -> Dict[str, Any]:
        """
        获取指定日历信息
        
        Args:
            calendar_id: 日历ID
            
        Returns:
            日历信息
        """
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取日历信息失败: {result.get('msg')}")
    
    def create_event(self, calendar_id: str, title: str, start_time: str, 
                     end_time: str, description: str = "", 
                     attendees: List[Dict[str, str]] = None) -> str:
        """
        创建日程
        
        Args:
            calendar_id: 日历ID
            title: 日程标题
            start_time: 开始时间（RFC3339格式）
            end_time: 结束时间（RFC3339格式）
            description: 日程描述
            attendees: 参会人列表
            
        Returns:
            日程ID
        """
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events"
        
        data = {
            "summary": title,
            "start_time": {"timestamp": start_time},
            "end_time": {"timestamp": end_time}
        }
        
        if description:
            data["description"] = description
        
        if attendees:
            data["attendee_ability"] = "can_see_others"
            data["attendees"] = attendees
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("event", {}).get("event_id")
        else:
            raise Exception(f"创建日程失败: {result.get('msg')}")
    
    def get_event(self, calendar_id: str, event_id: str) -> Dict[str, Any]:
        """
        获取日程详情
        
        Args:
            calendar_id: 日历ID
            event_id: 日程ID
            
        Returns:
            日程详情
        """
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events/{event_id}"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取日程详情失败: {result.get('msg')}")
    
    def list_events(self, calendar_id: str, start_time: str, end_time: str,
                   page_size: int = 50, page_token: str = None) -> Dict[str, Any]:
        """
        列出日程
        
        Args:
            calendar_id: 日历ID
            start_time: 开始时间（RFC3339格式）
            end_time: 结束时间（RFC3339格式）
            page_size: 每页数量
            page_token: 分页令牌
            
        Returns:
            日程列表
        """
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events"
        params = {
            "page_size": page_size
        }
        
        if page_token:
            params["page_token"] = page_token
        
        # 使用time_range参数
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events"
        params["time_range"] = f"{start_time}/{end_time}"
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取日程列表失败: {result.get('msg')}")
    
    def update_event(self, calendar_id: str, event_id: str, 
                     summary: str = None, start_time: str = None, 
                     end_time: str = None, description: str = None) -> bool:
        """
        更新日程
        
        Args:
            calendar_id: 日历ID
            event_id: 日程ID
            summary: 日程标题
            start_time: 开始时间
            end_time: 结束时间
            description: 日程描述
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events/{event_id}"
        
        data = {}
        if summary:
            data["summary"] = summary
        if start_time:
            data["start_time"] = {"timestamp": start_time}
        if end_time:
            data["end_time"] = {"timestamp": end_time}
        if description:
            data["description"] = description
        
        response = requests.patch(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        return result.get("code") == 0
    
    def delete_event(self, calendar_id: str, event_id: str) -> bool:
        """
        删除日程
        
        Args:
            calendar_id: 日历ID
            event_id: 日程ID
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/calendar/v4/calendars/{calendar_id}/events/{event_id}"
        response = requests.delete(url, headers=self._get_headers())
        result = response.json()
        
        return result.get("code") == 0
    
    def get_free_busy(self, user_ids: List[str], start_time: str, end_time: str) -> List[Dict[str, Any]]:
        """
        查询用户忙闲状态
        
        Args:
            user_ids: 用户ID列表
            start_time: 开始时间（RFC3339格式）
            end_time: 结束时间（RFC3339格式）
            
        Returns:
            用户忙闲状态列表
        """
        url = f"{self.base_url}/calendar/v4/free_busy/busy_time/query"
        data = {
            "user_ids": user_ids,
            "time_range": {
                "start": start_time,
                "end": end_time
            }
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("user_busy_time_list", [])
        else:
            raise Exception(f"查询忙闲状态失败: {result.get('msg')}")
    
    def create_calendar(self, name: str, description: str = "", 
                       color: str = "blue") -> str:
        """
        创建日历
        
        Args:
            name: 日历名称
            description: 日历描述
            color: 日历颜色
            
        Returns:
            日历ID
        """
        url = f"{self.base_url}/calendar/v4/calendars"
        data = {
            "summary": name,
            "description": description,
            "color": color
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("calendar", {}).get("calendar_id")
        else:
            raise Exception(f"创建日历失败: {result.get('msg')}")
    
    def search_events(self, calendar_id: str, query: str) -> List[Dict[str, Any]]:
        """
        搜索日程
        
        Args:
            calendar_id: 日历ID
            query: 搜索关键词
            
        Returns:
            日程列表
        """
        # 先列出所有日程，然后筛选
        all_events = self.list_events(calendar_id, "2020-01-01T00:00:00+08:00", "2030-12-31T23:59:59+08:00")
        filtered_events = []
        
        for event in all_events.get("items", []):
            summary = event.get("summary", "")
            description = event.get("description", "")
            
            if query.lower() in summary.lower() or query.lower() in description.lower():
                filtered_events.append(event)
        
        return filtered_events
