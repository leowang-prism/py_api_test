import requests
from utils.request_util import RequestUtil

class PostsApi:
    """帖子相关的API封装类"""
    def __init__(self):
        self.request_util = RequestUtil()
        self.base_url = self.request_util.get_base_url()

    def get_post(self, post_id):
        """
        获取单个帖子
        :param post_id: 帖子ID
        :return: Response对象
        """
        url = f"{self.base_url}/posts/{post_id}"
        return self.request_util.send_request("GET", url)

    def create_post(self, title, body, user_id):
        """
        创建新帖子
        :param title: 帖子标题
        :param body: 帖子内容
        :param user_id: 用户ID
        :return: Response对象
        """
        url = f"{self.base_url}/posts"
        data = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        return self.request_util.send_request("POST", url, json=data)

    def update_post(self, post_id, title, body, user_id):
        """
        更新帖子
        :param post_id: 帖子ID
        :param title: 新标题
        :param body: 新内容
        :param user_id: 用户ID
        :return: Response对象
        """
        url = f"{self.base_url}/posts/{post_id}"
        data = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        return self.request_util.send_request("PATCH", url, json=data)

    def delete_post(self, post_id):
        """
        删除帖子
        :param post_id: 帖子ID
        :return: Response对象
        """
        url = f"{self.base_url}/posts/{post_id}"
        return self.request_util.send_request("DELETE", url)