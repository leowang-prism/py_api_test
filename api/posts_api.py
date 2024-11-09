import requests
from utils.request_util import RequestUtil
from utils.log_util import logger

class PostsApi:
    """帖子相关的API封装类"""
    def __init__(self):
        self.request_util = RequestUtil()
        self.base_url = self.request_util.get_base_url()
        logger.info("PostsApi 初始化完成")

    def get_post(self, post_id):
        """获取单个帖子"""
        logger.info(f"获取帖子 ID: {post_id}")
        url = f"{self.base_url}/posts/{post_id}"
        return self.request_util.send_request("GET", url)

    def create_post(self, title, body, user_id):
        """创建新帖子"""
        logger.info("创建新帖子")
        logger.debug(f"标题: {title}, 内容: {body}, 用户ID: {user_id}")
        
        url = f"{self.base_url}/posts"
        data = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        return self.request_util.send_request("POST", url, json=data)

    def update_post(self, post_id, title, body, user_id):
        """更新帖子"""
        logger.info(f"更新帖子 ID: {post_id}")
        logger.debug(f"新标题: {title}, 新内容: {body}, 用户ID: {user_id}")
        
        url = f"{self.base_url}/posts/{post_id}"
        data = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        return self.request_util.send_request("PATCH", url, json=data)

    def delete_post(self, post_id):
        """删除帖子"""
        logger.info(f"删除帖子 ID: {post_id}")
        url = f"{self.base_url}/posts/{post_id}"
        return self.request_util.send_request("DELETE", url)