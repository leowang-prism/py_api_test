from utils.request_util import RequestUtil
from utils.log_util import logger
from common.exceptions import APIException

class BaseAPI:
    def __init__(self):
        self.request = RequestUtil()
        self.base_url = self.request.get_base_url()

    def send_request(self, method, path, **kwargs):
        """发送请求的基础方法"""
        url = f"{self.base_url}{path}"
        try:
            response = self.request.send_request(method, url, **kwargs)
            self._log_request_info(method, url, kwargs, response)
            return response
        except Exception as e:
            logger.error(f"API请求失败: {str(e)}")
            raise APIException(f"API请求失败: {str(e)}")

    def _log_request_info(self, method, url, kwargs, response):
        """记录请求信息"""
        logger.info(f"Request: {method} {url}")
        logger.debug(f"Headers: {kwargs.get('headers')}")
        logger.debug(f"Params: {kwargs.get('params')}")
        logger.debug(f"Data: {kwargs.get('data')}")
        logger.info(f"Response Status: {response.status_code}")
        logger.debug(f"Response Body: {response.text}") 