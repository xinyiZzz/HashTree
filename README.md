## March 1 2017 10:48 AM

# HashTree
Create a hash tree based on the URL for local storage and retrieval of web page information in the crawler/基于URL构建哈希目录树，用于爬虫中网页信息本地存储及检索

* * *


## Function/功能

为大量URL对应文件的存储及查询解决方案，应用于单域名下对应多个URL的情况
根据URL建立索引，通过对大量URL按照域名分目录存储，实现当一个域名下有大量URL时，能够通过域名和URL的哈希值快速定位到指定URL对应的目录
针对URL对应文件的不同版本在哈希目录树通过时间戳命名最后一层目录
用域名和URL哈希值共同作为目录名称，解决了无法直接用URL作为目录名称的问题

## Introduction/介绍

基于Hash目录树的存储技术使用了哈希思想和字典树的思想，即字典树中的最长前缀匹配思想，每一个文件夹作为树中的节点，树的层数即文件夹的层数取决为截取的位数

首先，将该字符串进行MD5哈希处理，得到一个固定长度32位的十六进制字符串值，再对这个32位的字符串分别对每8位截取，以每8位哈希值以字典树的形式建立并命名文件夹，共分为4层。例如，一个域名经哈希处理后得到的哈希值为2hsa3hcs24hvd4jsd4hsc3rvsdf73hs8，截取前8位2hsa3hcs，查询是否存在该文件夹，若存在则进入该文件夹，继续查询是否存在24hvd4js文件夹，若仍然存在则进入该文件夹继续查询；否则则依次建立2hsa3hcs之后哈希值对应文件夹。若进入最后一层文件夹sdf73hs8仍存在，则证明该URL存在


## Use examples/使用范例
```
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
```

## contact/联系方式


609610350@qq.com
