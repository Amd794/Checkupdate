# README
*****
[![py35,py36](https://img.shields.io/badge/Python-3.5|3.6,3|7-green.svg)](https://github.com/Amd794)

# 支持平台
- [x] 类似漫画台
- [x] 类似土豪漫画网站
- [x] 腾讯漫画
- [x] 腾讯视频
- [x] 好人卡
- [x] 自定义


# 安装
下载代码
```
git clone https://github.com/Amd794/Checkupdate.git
```
安装库文件
```python
pip3 install -r requirements.txt -i http://pypi.douban.com/simple
```
自定义订阅内容并初始化邮箱
```
cd Checkupdate
vi settings.py
```
新建一个check_update_comic.json文件。
运行
```python
python checkupdate.py
```
启动定时任务
```python
nohup python -u checkupdate.py > checkupdate.log 2>&1 &
```
更多介绍请移步: https://www.cnblogs.com/Mifen2952277346/p/10849966.html
*****
