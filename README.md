# miniSpider
a mini spider using python

usage:
<br />
python mini_spider.py -c spider.conf

spider.conf:
<br/>
[spider]
<br/>
url_list_file : ./urls ; 种子文件路径
<br/>
output_directory: ./output ; 抓取结果存取目录
<br/>
max_depth: 1 ; 抓取深度
<br/>
crawl_interval: 1; 抓取间隔
<br/>
crawl_timeout: 1; 抓取超时
<br/>
taget_url: .*.(html|html)$ ;需要抓取的url pattern
<br/>
thread_count: 8; 抓取线程

