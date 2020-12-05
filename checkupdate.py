# !/usr/bin/python3
# -*- coding: utf-8 -*-
# Time    : 2019/5/4 22:41
# Author  : Amd794
# Email   : 2952277346@qq.com
# Github  : https://github.com/Amd794

# nohup python -u checkupdate.py > checkupdate.log 2>&1 &
import re
import sys
from pathlib import Path

BASEDIR = Path().absolute()
sys.path.append(BASEDIR)

import time
import requests
from pyquery import PyQuery
import json
import traceback
from SendEmail import SendEmail
import os


def get_response(url, error_file_path='.', max_count=5, timeout=15, encoding='utf-8', name=''):
    header = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1 Edg/85.0.4183.83',
    }
    count = 0
    while count < max_count:
        try:
            response = requests.get(url=url, headers=header, timeout=timeout)
            response.raise_for_status()  # 如果status_code不是200,产生异常requests.HTTPError
            response.encoding = encoding
            return response
        except requests.exceptions.RequestException:
            # print(f'{url}连接超时, 正在进行第{count + 1}次连接重试, 等待响应时间为{timeout}秒')
            count += 1
    else:
        print(f'{url}重试{max_count}次后依然连接失败, 放弃连接...')
        if not os.path.exists(error_file_path):
            os.makedirs(error_file_path)
        with open(os.path.join(error_file_path, 'error_urls.txt'), 'a') as f:
            f.write(url + ' ' + name + '\n')
        return None


class Comic(object):
    def __init__(self):
        similar_selector_1 = '#detail-list-select > li:last'
        similar_selector_2 = '#chapterList > li:last > a'
        similar_selector_3 = '.panel-body .row div a:last'
        self.css_selector = {
            'kanleying': {
                'chapter_title_selector': similar_selector_1,
                'chapter_url_selector': f'{similar_selector_1} a',
            },
            'mm820': {
                'chapter_title_selector': similar_selector_2,
                'chapter_url_selector': similar_selector_2,
            },
            'comic_18': {
                'chapter_title_selector': similar_selector_3,
                'chapter_url_selector': similar_selector_3,
            },
        }

    def get_chapter_status(self, website_platform, comic_url):
        r = get_response(comic_url)
        pq = PyQuery(r.text)
        try:
            host_url = re.match('https?://\w+\.(.*?)\.\w+/', comic_url).group()
        except AttributeError:
            host_url = re.match('https?://(.*?)\.\w+/', comic_url).group()
        chapter_title_selector = self.css_selector.get(website_platform)['chapter_title_selector']
        chapter_url_selector = self.css_selector.get(website_platform)['chapter_url_selector']
        latest_chapter_title = pq(chapter_title_selector).text()
        latest_chapter_url = pq(chapter_url_selector).attr('href')
        latest_chapter_url = host_url + latest_chapter_url
        return latest_chapter_title, latest_chapter_url


def main():
    data_json = 'datas.json'
    check_update_comic_json = 'check_update_comic.json'
    template_html = 'template.html'
    # 判断该路径是否存在某文件
    if not os.access(data_json, os.F_OK):
        print(f'-----{data_json}不存在------')
        with open(data_json, 'w', encoding='utf-8') as fw:
            fw.write('{}')
    if not os.access(check_update_comic_json, os.F_OK):
        print(f'-----{check_update_comic_json}不存在------')
        with open(check_update_comic_json, 'w', encoding='utf-8') as fw:
            fw.write('''{
  'comic_18': {
  },
  'kanleying': {
    # 可配置符合这一类规则（选择器可获取到数据）的漫画平台
    '不一样的她': 'https://www.feixuemh.com/cartoon/3665',
  },
  'mm820': {
  }
}''')

    with open(data_json, encoding='utf-8') as fr:  # 读取本地漫画状态
        datas = json.load(fr)
    with open(check_update_comic_json, encoding='utf-8') as f:  # 获取监测的漫画
        DETAIL_DICT = eval(f.read())
    send_mail = SendEmail(emtype='htmlcontent')
    comic_obj = Comic()
    content = []
    for website_platform, comic in DETAIL_DICT.items():
        try:
            for comic_title, comic_url in comic.items():
                try:
                    obj = comic_obj.get_chapter_status(website_platform, comic_url)  # 获取漫画最新更新状态
                    if obj:
                        latest_chapter_title, latest_chapter_url = obj
                        new_data = latest_chapter_title  # 最新章节数据
                        old_data = datas.get(comic_title, None)  # 本地章节数据
                        if old_data != new_data:  # 判断是否有更新
                            datas[comic_title] = latest_chapter_title  # 更新本地章节

                            with open(template_html, encoding='utf-8') as f:
                                tx = f.read().format(url=comic_url, new_data=new_data, old_data=old_data,
                                                     comic_title=comic_title)  # 构造邮件内容
                                content.append(tx)
                            print(f"{comic_title} ---->{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} 更新")
                            # send_mail.sendEmail(content=tx, title=f'{website_platform}平台-{comic_title} 已更新',
                            #                     s=comic_title)  # 发送邮件, 推送更新

                            with open(data_json, 'w', encoding='utf-8') as fw:  # 存储更新后的状态
                                json.dump(datas, fw, ensure_ascii=False, indent=4, separators=(', ', ': '))
                        else:
                            pass
                except Exception:
                    print(traceback.format_exc())
        except TypeError as e:
            print(e)
            print(traceback.format_exc())
    if content:
        send_mail.sendEmail(content=''.join(content), title=f'漫画更新通知', s='\n推送更新')  # 发送邮件, 推送更新
    del send_mail
    tm = time.localtime()
    print(time.strftime('%Y-%m-%d %H:%M:%S', tm).center(65, '-'))
    print()


if __name__ == '__main__':
    while True:
        main()
        time.sleep(60 * 60 * 2)
