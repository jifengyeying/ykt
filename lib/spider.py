import requests
from bs4 import BeautifulSoup as bs
import re
import mypy.data
import mypy.download
import datetime


class NoSettingException(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return '你还没有设置或选择!'


# 这里是高三专用代码，高一高二是下面的
def gaosan(choice, class_='高三理科', data_path_name='data', aria2path=r'.\aria2c.exe'):
    print(choice)
    if not mypy.data.read_data('cookie', data_path_name=data_path_name):
        raise NoSettingException
    time = datetime.datetime.now().date().strftime('%m%d')
    li_dict = {'高三理科数学':'ma_l_3'}
    wen_dict = {'高三文科数学':'ma_w_3'}
    dict_ = {'地理':'go_3', '语文':'cn_3', '物理':'ph_3', '英语':'en_3', '政治':'zz_3', '历史':'hi_3', '化学':'ch_3', '生物':'bo_3'}
    dict_.update(li_dict if class_.find('文') == -1 else wen_dict)
    for i in dict_.keys():
        if choice == '所有':
            url = 'http://vd.mincoo.com:8088/jyyz/' + time + '/' + dict_.get(i) + '.mp4'
            mypy.download.aria2(dict_.get(i) + '.mp4', url, aria2path=aria2path, referer='http://ykt.zenking.cc/')
        else:
            if i.find(choice) != -1:
                url = 'http://vd.mincoo.com:8088/jyyz/' + time + '/' + dict_.get(i) + '.mp4'
                mypy.download.aria2(dict_.get(i) + '.mp4', url, aria2path=aria2path, referer='http://ykt.zenking.cc/')


class ykt:
    def __init__(self, data_path_name='data'):
        # 从浏览器截取到的一些信息
        headers = {'Host': 'ykt.zenking.cc', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Referer': '', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Cookie': ''}
        video_headers = {'Host': 'ykt.zenking.cc', 'Connection': 'keep-alive', 'Content-Length': '28', 'Accept': 'text/plain, */*; q=0.01', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Origin': 'http://ykt.zenking.cc', 'Referer': '', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Cookie': ''}
        # 读取信息
        headers['Cookie'] = mypy.data.read_data('cookie', data_path_name=data_path_name)
        video_headers['Cookie'] = mypy.data.read_data('cookie', data_path_name=data_path_name)
        if not headers['Cookie']:
            raise NoSettingException
        self.headers = headers
        self.video_headers = headers
        self.aria2path = r'.\lib\aria2c.exe'
        self.time = datetime.datetime.now().date()
        # 获取时间并去掉前面的0
        self.time_without_zero = str(int(self.time.strftime('%m'))) + '月' + str(int(self.time.strftime('%d')))

    def main(self, choice_num=None, class_=None):
        # 下载，choice要求列表(支持多个)!
        for num in choice_num:
            html_url = 'http://ykt.zenking.cc/uc/play/' + num + '/0'
            print(html_url)
            # 设置Referer
            self.headers['Referer'] = 'http://ykt.zenking.cc/front/couinfo/' + num
            self.video_headers['Referer'] = 'http://ykt.zenking.cc/uc/play/' + num + '/0'
            filename, urls = self.get_video_real_name_and_url(html_url, class_)
            self.download(urls, filename)

    def download(self, download_url, filename):
        # 调用aria2批量下载
        if download_url != -1:
            # 可能一天有多个视频
            for i in range(len(download_url)):
                # 因为使用的是命令行，使用不能有空格，要加上""
                mypy.download.aria2(name='"'+filename[i]+download_url[i][-4:]+'"', url=download_url[i],
                                    aria2path=self.aria2path, referer="http://ykt.zenking.cc")

    def get_video_real_name_and_url(self, html_url, class_):
        # 用beautifulsoup是因为他的find_all函数很好用，然后通过分析得到规律，抓取信息
        html = bs(requests.get(url=html_url, headers=self.headers).text, 'html.parser')
        video = re.findall(r"getPlayerHtml\((.+?)\)",
                           str(html.find_all("a", href="javascript:void(0)")))
        # 上面的是全部视频，这个是对应年级对应时间的
        video_class_today = []
        # 这里的find()会输出字符所在位置，没有时为-1，而不是True或False
        for i in video:
            if str(i).find(self.time_without_zero) != -1:
                if str(i).find(class_) != -1:
                    video_class_today.append(i)
        # 注意注意 这里不能写成a=b=[]的形式!!!
        kpointIds = []
        file_name = []
        urls = []
        # 获取kpointIds和file_name
        for i in video_class_today:
            a = str(i).split(',')
            kpointIds.append(a[0])
            # 他的名字是类似'2月26日\t高一\t数学期末试题评讲'的，所以要去掉\t和'
            # 并且这里需要注意的是因为str.replace方法是由c语言写的，所以不能用形参，只能用位参，并且这里的\t也不用转义
            file_name.append(a[2].replace('\t', '').replace("'", ''))
        # 得到id之后获取视频真实链接
        for kpointId in kpointIds:
            data = (('kpointId', kpointId), ('playFromType', '2'))
            # 这里本来用正则表达式更好，可惜我不怎么会
            u = str(bs(requests.post(url="http://ykt.zenking.cc/front/ajax/checkKpoint", data=data,
                                     headers=self.video_headers).text, 'html.parser'))
            # 检查视频是否过期
            if u.find('.mp4') != -1:
                urls.append(u[u.find('src=')+5:u.find('.mp4')] + '.mp4')
            elif u.find('courseKpoint/pdf/') != -1:
                urls.append(u[u.find('http://ykt.zenking.cc/images/upload/courseKpoint/pdf/'):u.find('.pdf')] + '.pdf')
            else:
                return -1,-1
        return file_name, urls


if __name__ == '__main__':
    a = dict(语文='193', 高一二数学='205', 英语='196', 物理='200', 化学='201', 生物='199',
         历史='197', 政治='202', 地理='198', 团课='204', 体育='210', 音乐='208', 心理='203', 美术='209')
    num = []
    for i in a.keys():
        num.append(a.get(i))

    spider = ykt(r'.\lib\data')
    print('高一')
    spider.main(choice_num=num, class_='高一')
    print('高三')
    gaosan('所有', '高三理科', 'data', r'.\lib\aria2c.exe')
