#!/usr/bin/python
#-*-coding:utf-8-*-
'''
Name: 基于URL构建哈希目录树，用于爬虫网页信息本地存储及检索
Author：XinYi 609610350@qq.com
Time：2015.6

模块介绍：
    为大量URL对应文件的存储及查询解决方案，应用于单域名下对应多个URL的情况
    根据URL建立索引，通过对大量URL按照域名分目录存储，实现当一个域名下有大量URL时，
    能够通过域名，和URL的哈希值快速定位到指定URL对应的目录。
    并针对URL对应文件的不同版本在哈希目录树通过时间戳命名最后一层目录
    并解决了无法直接用URL作为目录名称的问题，即用域名和URL哈希值共同作为目录名称
    参数注释：
        root_path  # 带域名的哈希目录树绝对路径，其下路径为/domain/hash…/…/timestamp，用于存储URL信息
        hash_path  # 不带域名的哈希目录树绝对路径，其下路径为/hash…/…/timestamp，用于URL去重
        layer_num  # 哈希目录树的层数
'''
import os
import time
import hashlib
from urlparse import urlparse
from os.path import join as pjoin

DEFAULT_LAYER_NUM = 4


def hash_md5(date):
    '''
    对给定数据以2048字符截断后分组进行MD5哈希，返回十六进制哈希值
    例如：1d6fee8f94b9e8edb5d7cb2aa8149aa0
    '''
    md5 = hashlib.md5()
    while True:
        temp = date[:2048]
        if temp == '':
            break
        else:
            md5.update(temp)
            date = date[2048:]
    return md5.hexdigest()


def get_hash_path(url, layer_num=DEFAULT_LAYER_NUM):
    '''
    对指定URL进行MD5哈希，用16进制哈希值以layer_num数截断后拼接为路径返回
    输出md5_path例如:  1d6fee8f/94b9e8ed/b5d7cb2a/a8149aa0
    '''
    md5_path = ''
    url_md5 = hash_md5(url)
    once_layer_len = len(url_md5) / layer_num
    for i in range(layer_num):
        if md5_path == '':
            md5_path = url_md5[0:once_layer_len]
        else:
            md5_path = pjoin(md5_path, url_md5[0:once_layer_len])
        url_md5 = url_md5[once_layer_len:]
    return md5_path


def get_web_hash_path(url, layer_num=DEFAULT_LAYER_NUM):
    '''
    获取网页的hash路径
    web_save_path例如：www.baidu.com/1d6fee8f/94b9e8ed/b5d7cb2a/a8149aa0
    '''
    host = urlparse(url).netloc  # 获取域名
    url_md5 = get_hash_path(url, layer_num)
    web_save_path = pjoin(host, url_md5)
    return web_save_path


def get_web_hash_path_abs(url, root_path, layer_num=DEFAULT_LAYER_NUM):
    '''
    获取网页的绝对hash路径
    例如：/home/zxy/www.baidu.com/1d6fee8f/94b9e8ed/b5d7cb2a/a8149aa0
    '''
    return pjoin(root_path, get_web_hash_path(url, layer_num))


def generate_timestamp_dir_name():
    '''
    生成时间戳目录名, 例如: 2016-04-01_22-40-52
    '''
    return time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))


def get_latest_timestamp_dir_name(web_save_path_abs):
    '''
    从绝对路径下获取最新的时间戳目录名称，本质为对文件夹按名称进行排序
    root_web_save_path例如：/home/zxy/www.baidu.com/1d6fee8f/94b9e8ed/b5d7cb2a/a8149aa0
    latest_timestamp_dir例如：2016-04-01 22_40
    '''
    web_save_timestamp_dir = os.listdir(web_save_path_abs)
    latest_timestamp_dir = sorted(web_save_timestamp_dir)[-1]
    return latest_timestamp_dir


def get_latest_timestamp_dir_abs(url, root_path, layer_num=DEFAULT_LAYER_NUM):
    '''
    获取指定URL最新的时间戳目录的绝对路径
    例如：/home/zxy/www.baidu.com/1d6fee8f/94b9e8ed/b5d7cb2a/a8149aa0/2016-04-01 22_40
    '''
    web_save_path_abs = get_web_hash_path_abs(url, root_path, layer_num)
    return pjoin(web_save_path_abs, get_latest_timestamp_dir_name(web_save_path_abs))


def recursion_dir_list(layer, path):
    '''
    递归遍历多层目录，并返回最后一层目录所有文件的绝对路径
    '''
    dir_list = os.listdir(path)
    new_dir_list = []
    if layer == 0:
        return [pjoin(path, dir_name) for dir_name in dir_list]
    else:
        for dir_name in dir_list:
            new_dir_list.extend(recursion_dir_list(
                layer - 1, pjoin(path, dir_name)))
        return new_dir_list


def get_hash_dir_info(root_path, layer_num=DEFAULT_LAYER_NUM):
    '''
    返回哈希目录树所有最后一层时间戳路径，并返回时间戳对应的文件列表
    例如:{'www.baidu.com/…':{'/home/…/2015-10-28 18_06':['css','js']}, 'url2':{}}
    即{URL:{时间戳路径:[文件列表], 时间戳路径:[文件列表]}, 'URL':[]}
    '''
    dir_list = recursion_dir_list(layer_num + 1, root_path)
    hash_dir_info = {}
    for path in dir_list:
        if 'url_file' not in os.listdir(path):
            continue
        with open(pjoin(path, 'url_file')) as f:
            url = f.readline().strip()
        if url not in hash_dir_info:
            hash_dir_info[url] = {path: os.listdir(path)}
        else:
            hash_dir_info[url][path] = os.listdir(path)
    return hash_dir_info


def exist_url_wipe_repeat(root_path, url_list, add_sign=False, layer_num=4):
    '''
    基于Hash目录树的URL去重，对输入的url_list去重返回不存在的URL列表
    add_sign为True，表示查询同时，对不存在的URL添加到Hash目录树中
    '''
    url_no_exist_list = []  # 储存hash目录树中不存在的url
    for url in url_list:
        hash_path = get_hash_path(url, layer_num)
        folder_list = hash_path.split('/')
        exist_flag = 1
        current_path = root_path  # 去重根路径
        for folder_name in folder_list:
            current_path = current_path + '/' + folder_name
            if os.path.exists(current_path):
                continue
            else:
                if add_sign:
                    os.mkdir(current_path)
                exist_flag = 0  # 目录不存在 标志位置为零
        if exist_flag == 0:
            url_no_exist_list.append(url)
    return url_no_exist_list


if __name__ == '__main__':
    # 根据url_list，读取web_info中指定URL对应的main.html路径
    root_path = '/home/eggtart'
    layer_num = 4
    print get_latest_timestamp_dir_abs('http://tabkytg.pw/main/pay_files/opay.html', root_path, layer_num)
    print get_web_hash_path('http://tabkytg.pw/main/pay_files/opay.html', layer_num)
    web_save_path_abs = get_web_hash_path_abs(
        'http://tabkytg.pw/main/pay_files/opay.html', root_path, layer_num)
    print web_save_path_abs
    print get_latest_timestamp_dir_name(web_save_path_abs)
    a = get_hash_dir_info(root_path, layer_num)
    for i in a:
        print i, a[i]
