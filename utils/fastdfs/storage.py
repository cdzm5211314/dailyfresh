# -*- coding:utf-8 -*-
# @Desc : 自定义文件(图片)存储类
# @Author : Administrator
# @Date : 2019-03-04 14:43

from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings


class FastDFSStorage(Storage):

    def __init__(self, client_conf=None, nginx_url=None):
        '''初始化操作'''
        if client_conf is None:
            # client_conf = './utils/fastdfs/client.conf'
            client_conf = settings.FDFS_CLIENT_CONFIG
        self.client_conf = client_conf

        if nginx_url is None:
            # nginx_url = 'http://192.168.208.128:8888/'
            nginx_url = settings.FDFS_NGINX_URL
        self.nginx_url = nginx_url

    def _open(self, name, mode='rb'):
        '''打开文件时使用'''
        pass

    def _save(self, name, content):
        '''保存文件时使用'''
        # name: 上传文件的名字
        # content: 包含上传文件内容的File对象
        # 创建Fdfs_client对象
        # client = Fdfs_client('./utils/fastdfs/client.conf')
        client = Fdfs_client(self.client_conf)

        # 上传文件到 fdfs系统总
        # result = client.upload_by_filename('test')
        result = client.upload_by_buffer(content.read())

        # 判断上传是否成功
        if result.get('Status') != 'Upload successed.':  # 上传失败
            raise Exception("上传文件到fdfs系统失败,请重新上传...")

        # 获取上传成功后返回的文件ID
        file_id = result.get('Remote file_id')
        return file_id

    def exists(self, name):
        '''django判断文件名是否可用'''
        return False

    def url(self, file_url):
        '''返回访问文件的url路径file_url = file_id'''
        # return file_url
        # return 'http://192.168.208.128:8888' + file_url
        return self.nginx_url + file_url
