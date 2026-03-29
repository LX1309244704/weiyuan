"""
飞书任务管理模块
"""
import requests
import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class TaskManager:
    """任务管理器"""
    
    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        初始化任务管理器
        
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
    
    def get_tasklists(self) -> List[Dict[str, Any]]:
        """
        获取任务清单列表
        
        Returns:
            任务清单列表
        """
        url = f"{self.base_url}/task/v2/tasklists"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("tasklist_items", [])
        else:
            raise Exception(f"获取任务清单失败: {result.get('msg')}")
    
    def create_tasklist(self, name: str, description: str = "") -> str:
        """
        创建任务清单
        
        Args:
            name: 清单名称
            description: 清单描述
            
        Returns:
            清单ID
        """
        url = f"{self.base_url}/task/v2/tasklists"
        data = {
            "name": name,
            "summary": description
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("tasklist", {}).get("tasklist_guid")
        else:
            raise Exception(f"创建任务清单失败: {result.get('msg')}")
    
    def get_tasklist(self, tasklist_guid: str) -> Dict[str, Any]:
        """
        获取任务清单详情
        
        Args:
            tasklist_guid: 任务清单ID
            
        Returns:
            任务清单详情
        """
        url = f"{self.base_url}/task/v2/tasklists/{tasklist_guid}"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取任务清单详情失败: {result.get('msg')}")
    
    def create_task(self, tasklist_guid: str, summary: str, 
                   description: str = "", due_time: str = None,
                   assignee: str = None) -> str:
        """
        创建任务
        
        Args:
            tasklist_guid: 任务清单ID
            summary: 任务标题
            description: 任务描述
            due_time: 截止时间（RFC3339格式）
            assignee: 负责人ID
            
        Returns:
            任务ID
        """
        url = f"{self.base_url}/task/v2/tasks"
        
        data = {
            "tasklist_guid": tasklist_guid,
            "summary": summary
        }
        
        if description:
            data["description"] = description
        
        if due_time:
            data["due"] = {
                "timestamp": due_time
            }
        
        if assignee:
            data["assignee"] = {
                "assignee_type": "user",
                "id": assignee
            }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("task", {}).get("task_guid")
        else:
            raise Exception(f"创建任务失败: {result.get('msg')}")
    
    def get_task(self, task_guid: str) -> Dict[str, Any]:
        """
        获取任务详情
        
        Args:
            task_guid: 任务ID
            
        Returns:
            任务详情
        """
        url = f"{self.base_url}/task/v2/tasks/{task_guid}"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取任务详情失败: {result.get('msg')}")
    
    def list_tasks(self, tasklist_guid: str, page_size: int = 50, 
                   page_token: str = None) -> Dict[str, Any]:
        """
        获取任务列表
        
        Args:
            tasklist_guid: 任务清单ID
            page_size: 每页数量
            page_token: 分页令牌
            
        Returns:
            任务列表
        """
        url = f"{self.base_url}/task/v2/tasks"
        params = {
            "tasklist_guid": tasklist_guid,
            "page_size": page_size
        }
        
        if page_token:
            params["page_token"] = page_token
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {})
        else:
            raise Exception(f"获取任务列表失败: {result.get('msg')}")
    
    def update_task(self, task_guid: str, summary: str = None,
                   description: str = None, due_time: str = None,
                   completed: bool = None) -> bool:
        """
        更新任务
        
        Args:
            task_guid: 任务ID
            summary: 任务标题
            description: 任务描述
            due_time: 截止时间
            completed: 是否完成
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/task/v2/tasks/{task_guid}"
        
        data = {}
        if summary:
            data["summary"] = summary
        if description:
            data["description"] = description
        if due_time:
            data["due"] = {
                "timestamp": due_time
            }
        if completed is not None:
            data["completed"] = "0" if completed else "1692664108750760"
        
        response = requests.patch(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        return result.get("code") == 0
    
    def delete_task(self, task_guid: str) -> bool:
        """
        删除任务
        
        Args:
            task_guid: 任务ID
            
        Returns:
            是否成功
        """
        url = f"{self.base_url}/task/v2/tasks/{task_guid}"
        response = requests.delete(url, headers=self._get_headers())
        result = response.json()
        
        return result.get("code") == 0
    
    def create_subtask(self, parent_task_guid: str, summary: str,
                      description: str = "") -> str:
        """
        创建子任务
        
        Args:
            parent_task_guid: 父任务ID
            summary: 子任务标题
            description: 子任务描述
            
        Returns:
            子任务ID
        """
        url = f"{self.base_url}/task/v2/subtasks"
        
        data = {
            "parent_task_guid": parent_task_guid,
            "summary": summary
        }
        
        if description:
            data["description"] = description
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("subtask", {}).get("task_guid")
        else:
            raise Exception(f"创建子任务失败: {result.get('msg')}")
    
    def get_subtasks(self, parent_task_guid: str) -> List[Dict[str, Any]]:
        """
        获取子任务列表
        
        Args:
            parent_task_guid: 父任务ID
            
        Returns:
            子任务列表
        """
        url = f"{self.base_url}/task/v2/subtasks"
        params = {
            "parent_task_guid": parent_task_guid
        }
        
        response = requests.get(url, headers=self._get_headers(), params=params)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("subtasks", [])
        else:
            raise Exception(f"获取子任务列表失败: {result.get('msg')}")
    
    def search_tasks(self, tasklist_guid: str, query: str) -> List[Dict[str, Any]]:
        """
        搜索任务
        
        Args:
            tasklist_guid: 任务清单ID
            query: 搜索关键词
            
        Returns:
            任务列表
        """
        # 先获取所有任务，然后筛选
        all_tasks = self.list_tasks(tasklist_guid)
        filtered_tasks = []
        
        for task in all_tasks.get("items", []):
            summary = task.get("summary", "")
            description = task.get("description", "")
            
            if query.lower() in summary.lower() or query.lower() in description.lower():
                filtered_tasks.append(task)
        
        return filtered_tasks
    
    def add_task_comment(self, task_guid: str, content: str) -> str:
        """
        添加任务评论
        
        Args:
            task_guid: 任务ID
            content: 评论内容
            
        Returns:
            评论ID
        """
        url = f"{self.base_url}/task/v2/tasks/{task_guid}/comments"
        data = {
            "content": content
        }
        
        response = requests.post(url, headers=self._get_headers(), json=data)
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("comment", {}).get("comment_id")
        else:
            raise Exception(f"添加评论失败: {result.get('msg')}")
    
    def get_task_comments(self, task_guid: str) -> List[Dict[str, Any]]:
        """
        获取任务评论列表
        
        Args:
            task_guid: 任务ID
            
        Returns:
            评论列表
        """
        url = f"{self.base_url}/task/v2/tasks/{task_guid}/comments"
        response = requests.get(url, headers=self._get_headers())
        result = response.json()
        
        if result.get("code") == 0:
            return result.get("data", {}).get("comments", [])
        else:
            raise Exception(f"获取评论列表失败: {result.get('msg')}")
