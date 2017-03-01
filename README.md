## March 1 2017 10:48 AM

# HashTree
Create a hash tree based on the URL for local storage and retrieval of web page information in the crawler/基于URL构建哈希目录树，用于爬虫中网页信息本地存储及检索

* * *


## system function/系统功能

为大量URL对应文件的存储及查询解决方案，应用于单域名下对应多个URL的情况
根据URL建立索引，通过对大量URL按照域名分目录存储，实现当一个域名下有大量URL时，
能够通过域名，和URL的哈希值快速定位到指定URL对应的目录。
并针对URL对应文件的不同版本在哈希目录树通过时间戳命名最后一层目录
并解决了无法直接用URL作为目录名称的问题，即用域名和URL哈希值共同作为目录名称

## Use examples/使用范例

root_path = '/home/phishing/phishing_check'
layer_num = 4

print get_latest_timestamp_dir_abs('http://tabkytg.pw/main/pay_files/opay.html', root_path, layer_num)

print get_web_hash_path('http://tabkytg.pw/main/pay_files/opay.html', layer_num)

web_save_path_abs = get_web_hash_path_abs('http://tabkytg.pw/main/pay_files/opay.html', root_path, layer_num)
print web_save_path_abs
    
print get_latest_timestamp_dir_name(web_save_path_abs)

a = get_hash_dir_info(root_path, layer_num)
for i in a:
  print i, a[i]


## contact/联系方式


609610350@qq.com
