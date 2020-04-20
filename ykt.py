import tkinter as tk
import tkinter.ttk as ttk
import mypy.data
import requests
from lib import spider
from lib import login_qiandao
from selenium import webdriver
choice_dict = dict(所有='all', 语文='193', 数学='205', 英语='196', 物理='200', 化学='201', 生物='199',
                                历史='197', 政治='202', 地理='198', 团课='204', 体育='210', 音乐='208', 心理='203', 美术='209')

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.aria2path = r'.\lib\aria2c.exe'
        self.data_path_name = './lib/data'
        self.all_value_dict = []
        for key in choice_dict.keys():
            if key == '所有':
                pass
            else:
                self.all_value_dict.append(choice_dict.get(key))

    def login_qiandao_window(self):
        set_1 = tk.Toplevel(self)
        set_1.title('登录')

        self.user = tk.StringVar()
        self.pwd = tk.StringVar()

        user_frame = tk.Frame(set_1)
        tk.Label(user_frame, text='账号:').pack(side='left')
        tk.Entry(user_frame, bd=2, textvariable=self.user).pack(side='right')
        user_frame.pack()

        pwd_frame = tk.Frame(set_1)
        tk.Label(pwd_frame, text='密码:').pack(side='left')
        tk.Entry(pwd_frame, bd=2, textvariable=self.pwd).pack(side='right')
        pwd_frame.pack()

        botton_frame = tk.Frame(set_1)
        tk.Button(botton_frame, text='登录', command=self.login).pack(side='left')
        # tk.Button(botton_frame, text='签到', command=self.qiandao).pack(side='left')
        tk.Button(botton_frame, text='签到(chrome版)', command=self.qiandao_chrome).pack(side='right')
        botton_frame.pack(side='bottom')

    def login(self):
        cookie = login_qiandao.login(self.user.get(), self.pwd.get())
        if cookie:
            mypy.data.write_data(data_path_name=self.data_path_name, cookie=cookie)

    def qiandao(self):
        pass

    def qiandao_chrome(self):
        all_value_dict = self.all_value_dict
        all_value_dict.extend(['194', '195'])
        user = self.user.get()
        pwd = self.pwd.get()
        if (user and pwd):
            browser = webdriver.Chrome(r'.\lib\chromedriver.exe')
            url = 'http://ykt.zenking.cc/front/couinfo/193'
            browser.get(url)
            browser.find_element_by_css_selector('#cou-shopcar[title="签到"]').click()
            browser.find_element_by_css_selector('input#u-email').send_keys(user)
            browser.find_element_by_css_selector('input#u-password').send_keys(pwd)
            browser.find_element_by_css_selector('a.e-login-btn').click()
            for i in all_value_dict:
                url = 'http://ykt.zenking.cc/front/couinfo/' + i
                browser.get(url)
                browser.find_element_by_css_selector('#cou-shopcar[title="签到"]').click()
        self.login()

    def setting_window(self):
        set_ = tk.Toplevel(self)
        set_.title('高级设置')
        label = tk.Label(set_, text='非专业人员撤退！\n为了防止某一天登录程序失效备下的').pack(side='top')

        self.cookie = tk.StringVar()

        cookie_frame = tk.Frame(set_)
        tk.Label(cookie_frame, text='Cookie:').pack(side='left')
        tk.Entry(cookie_frame, bd=2, textvariable=self.cookie).pack(side='right')
        cookie_frame.pack()

        tk.Button(set_, text='设置', command=self.setting).pack(side='bottom')

    def setting(self):
        mypy.data.write_data(
            data_path_name=r'.\lib\data',
            cookie=self.cookie.get()
        )

    def about(self):
        about_ = tk.Toplevel(self)
        about_.title('关于')
        tk.Label(about_, text='--禅境网课下载--2.0bata by yokn').pack(anchor='n')
        tk.Label(about_, text='此网课下载器很多都是观察规律的，所以如果网站改了会失效').pack()
        tk.Label(about_, text='本人技术有限，如果有大佬愿意交流，\n或者有问题(1079687566)').pack()
        tk.Label(about_, text='祝各位同学成绩理想!（').pack()
        tk.Label(about_, text='\n---问题---').pack()
        tk.Label(about_, text='为什么是bata版?\n因为签到功能还不完善,测试人数少\n那哪个时候有2.0稳定版本?\n以后每天开发者只会以极少的时间更新\n所以只能...期待吧(').pack()
        tk.Label(about_, text='\n---更新日志---').pack()
        tk.Label(about_, text='2.0 支持pdf和高三数学，签到需要chrome 81版\nhttps://www.google.cn/intl/zh-CN/chrome').pack()
        tk.Label(about_, text='1.1 更优美的代码，支持登录，封装得更小白了，耗费作者大量时间').pack()

    def create_widgets(self):
        menubar = tk.Menu(self)
        menubar.add_command(label='登录/签到', command=self.login_qiandao_window)
        menubar.add_command(label='高级设置', command=self.setting_window)
        menubar.add_command(label='关于', command=self.about)
        self.master.config(menu=menubar)

        self.label = tk.Label(self)
        self.label["text"] = '--禅境网课下载--\n(使用新版本前请看关于然后进行登录!)'
        self.label.pack(anchor='n')

        self.combobox_choice = ttk.Combobox(self, value=tuple(choice_dict.keys()))
        self.combobox_choice.pack()

        self.combobox_class = ttk.Combobox(self, value=('高一', '高二', '高三文科','高三理科'))
        self.combobox_class.pack()

        self.down = tk.Button(self)
        self.down["text"] = "下载(全部)"
        self.down["command"] = self.download
        self.down.pack(anchor='center')

        self.quit = tk.Button(self, text="退出", fg="red",
                              command=self.master.destroy)
        self.quit.pack(anchor='s')

    def download(self):
        if self.combobox_class.get().find('高三') != -1:
            spider.gaosan(choice=self.combobox_choice.get(), class_ = self.combobox_class.get(), data_path_name=self.data_path_name, aria2path=self.aria2path)
        else:
            choice = []
            # 如果是所有则遍历，否则直接找到值
            if self.combobox_choice.get() == '所有':
                choice = self.all_value_dict
            else:
                choice.append(choice_dict.get(self.combobox_choice.get()))
            ykt = spider.ykt(data_path_name=self.data_path_name)
            ykt.main(choice_num=choice, class_=self.combobox_class.get())



if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
