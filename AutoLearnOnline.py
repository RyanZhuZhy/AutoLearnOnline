# -*- coding:utf-8 -*-


import http.cookiejar
import re
import time
import urllib.parse
import urllib.request
from urllib.request import Request
from urllib.request import urlopen


class AutoLearnOnline():

    def __init__(self):
        print("欢迎使用自动在线学习工具！")
        print("本工具用于以下两个网站自动在线学习：")
        print("1.金华市公务员网络学院")
        print("2.浙江省领导干部学院金华分院")
        print("（注意：在使用本工具前，请先手动完成选课）")
        self.web = input("请选择学习网站(输入1或2）：")
        if self.web not in ['1','2']:
            print("无效输入！！")
            exit(0)

        self.username = input("请输入用户名：")
        self.password = input("请输入密码：")

        #test data
        #self.web = '1'
        #self.username = '18857911606'
        #self.password = '666666'
        #self.username = '13566995759'
        #self.password = '82469377'
        
        # All url path
        if self.web == '1':
            self.web_url = r"http://jhpx.net:8001/"
            
            self.login_params = {
                "__VIEWSTATE": "/wEPDwULLTE1ODQwMDcwOTVkGAEFHl9fQ29udHJ"
                               "vbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYDBRBjdG"
                               "wwNSRjYlJlbWVtYmVyBRFjdGwwNSRMb2dpbkJ1d"
                               "HRvbgUUY3RsMDUkUmVnaXN0ZXJCdXR0b27SH11C"
                               "vnRTGZb6B+RenDFvb9ynZg==",
                "__EVENTVALIDATION": "/wEWCAKxxYOLCwKBpvHtBQLNjcIzAvX5l"
                                     "P0DApzilpYDAuar7KIEApvstOsHAvr2td"
                                     "4IjFELx5ZqaYNVDNyBg8/Ue3gRvZo=",
                "hidPageID": "268",
                "ctl05$hdIsDefault": "0",
                "ctl05$UserName": self.username,
                "ctl05$Password": self.password,
                "ctl05$LoginButton.x": "30",
                "ctl05$LoginButton.y": "10",
                "select1": "#",
                "select2": "#",
                "select4": "#",
                "select3": "#",
                "select5": "#"
            }

            self.user_ru = '欢迎您：<b>(.*?)</b></span>'
            self.courses_ru = 'list4.*?ndow.*?id=(.*?)&user_id=(.*?)"'
        elif self.web == '2':
            self.web_url = r"http://jhce.jhxf.gov.cn:80/"

            self.login_params = {
                "__EVENTTARGET":"",
                "__EVENTARGUMENT":"",
                "__VIEWSTATE":r"/wEPDwUJNTEzNjUwMDgwZBgBBR5fX0NvbnRyb2x"
                               "zUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUgY3RsMD"
                               "AkY3AkTG9naW4xJExvZ2luSW1hZ2VCdXR0b24FE"
                               "2N0bDAwJGNwJGNiUmVtZW1iZXJRV1pKVV/XJayu"
                               "PUVpyxzRHyRKlA==",
                "__EVENTVALIDATION":r"/wEWBQLz4vLLDALEmrPyBwK5t6XjAwLst"
                                     "N++DALhyKDQDqJisht6spPM44gkmVmV+2"
                                     "+hSw5u",
                "ctl00$cp$Login1$UserName": self.username, 
                "ctl00$cp$Login1$Password": self.password,
                "ctl00$cp$Login1$LoginButton": " 登  录 ", 
                "select": "省（区市）政府机关网站",
                "select3": "省（区市）高等院校网站",
                "select4": "相关培训机构网站"
            }
            
            self.user_ru = '欢迎您：<span class="r_red">(.*?)</span>'
            self.courses_ru = ('<tr class="table2.*?middle" class="tabl'
                'e2">(.*?)</td.*?ndow.*?id=(.*?)&user_id=(.*?)"')
        
        self.login_url = self.web_url + "login.aspx"
        self.courses_url = self.web_url + "My/MyCourse.aspx?type=1"
        self.clear_url = self.web_url + "play/clear.ashx"
        self.aicc_url = self.web_url + "play/AICCProgressnew.ashx"

        # All rule
        self.kick_ru = "是否踢出.*?location='(.*?)';}else"
        self.section_ru = ('"SID":"(.*?)", "lastLocation":"(.*?)","stat'
                           'e":"(.*?)" ,"duration":"(.*?)"')
        self.course_name_ru = '/lessionnew/gc/(.*?)/index'
        self.lesson_title_ru = 'LessonTitle="(.*?)" Course'
        #self.stime_ru = ('ScoTitle="(.*?)" is.*?maxTime="(.*?)" swf_url'
        #                 '="(.*?)" flv_url="(.*?)"/>')
        self.stime_ru = ('ScoTitle="(.*?)" is.*?minTime="(.*?)" ma.*?'
                         'swf_url="(.*?)" flv_url="(.*?)"/>')
        #self.charset_ru = 'charset=(.*?)"'
        
        # HTTP headers
        self.user_agent = ("Mozilla/5.0 (Windows NT 5.1) AppleWebKit"
                           "537.36 KHTML, like Gecko) Chrome/50.0.26"
                           "61.102 Safari/537.36")
        self.content_type = 'application/x-www-form-urlencoded'
        self.headers = {'Connection': 'keep-alive',
                        'User-Agent': self.user_agent} 
        
        # init Cookie
        self.cj = http.cookiejar.CookieJar()
        self.my_cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(self.opener)

        self.keep_clear = True
        self.encode = 'utf-8'
        self.cookie = ""

        self.user_id = ""
        self.user_name = ""
        self.course_id = ""
        self.course_name = ""

    def save(self, response):
        with open("111.txt", "wb") as f:
            f.write(response)

    def find(self, ru, string, encode=""):
        if not encode:
            encode = self.encode
        return re.findall(ru, string.decode(encode, 'ignore'), re.S)

    def login(self):     
        params = urllib.parse.urlencode(self.login_params).encode('utf-8')
        request = Request(self.login_url, params, 
            self.headers, method="POST")
        response = urlopen(request, timeout=120).read()
        
        items = self.find(self.kick_ru, response)
        if items:
            response = urlopen(items[0]).read()
        user = self.find(self.user_ru, response)
        if user:
            print("登陆成功: %s" % user[0])
            #self.my_cj = copy.deepcopy(self.cj)
        else:
            self.save(response)
            print("登陆失败！！")
            exit(0)

    def getcourses(self):
        # Get courses list
        #print(self.cj)
        #print(self.my_cj)

        response = urlopen(self.courses_url).read()
        courses = self.find(self.courses_ru, response)

        if not courses:
            print("课程列表为空，请先手动选课！")
            self.save(response)
            return False
        
        course = courses[0]

        if self.web == '1':
            self.user_id = self.username
            self.course_id = course[0]
            self.user_name = self.username        
        elif self.web == '2':
            self.user_id = course[2]
            self.course_id = course[1]
            self.user_name = course[2]

        url = (self.web_url + "play/redirect.aspx?id=" +
               self.course_id + "&user_id=" + self.user_id)
        response = urlopen(url).read()
        items = self.find(self.course_name_ru, response)
        if not items:
            self.save(response)
            print("获取courseName参数失败！")
            exit(0)
        self.course_name = items[0]
        return True

    def progressbar(self, sid, second):
        #bar_length = 20
        for i in range(20):
            bar = '*' * i + ' ' * (21-i) + str(i * 5) + '%'
            print("\r第%s节（共%3s秒）：%s" % (sid, second, bar), end=" ")
            time.sleep(second/20)
        bar = '*' * 20 + ' ' + '完成'
        print("\r第%s节（共%3s秒）：%s" % (sid, second, bar))

    def sendclear(self):
        # Send clear
        while self.keep_clear:
            url = (self.clear_url + "?course_id=" + self.course_id + "&"
                   + str(random.random()))
            headers = {'Accept': '*/*',
                       'Accept-Encoding': 'gzip, deflate, sdch',
                       'Accept-Language': 'zh-CN,zh;q=0.8',
                       'Connection': 'keep-alive',
                       'Content-Type': 'application/x-www-form-urlencoded',
                       'User-Agent': self.user_agent,
                       'Host': 'jhce.jhxf.gov.cn',
                       'Referer': (self.web_url + 'play/play.aspx?' +
                                   'course_id=' + self.course_id),
                       'X-Requested-with': 'XMLHttpRequest'}
            request = Request(url, headers=headers)
            response = urlopen(url, timeout=120).read()
            if response.decode(self.encode) != 'ok':
                print(response.decode(self.encode))
            time.sleep(4)

    def playcourse(self):
        #auto_clear = threading.Thread(target=self.sendclear)
        #auto_clear.start()
        
        # SCO.html
        url = (self.web_url + "lessionnew/gc/" + self.course_name + 
               "/SCO.html?URL=jhce.jhxf.gov.cn:80/play/" + 
               "AICCProgressnew.ashx&userID=" + self.user_id +
               "&courseID=" + self.course_id + "&userName=" + 
               self.user_name + "&courseName=" + self.course_name +
               "&go=0")
        headers = {
            'Accept': ('text/html,application/xhtml+xml,application/xml'
                       ';q=0.9,image/webp,*/*;q=0.8'),
            'Upgrade-Insecure-requests': '1',
            'User-Agent': self.user_agent,
            'Connection': 'keep-alive',
            'Referer': url,
            'X-Requested-With': 'ShockwaveFlash/21.0.0.182'
        }
        request = Request(url, headers=headers)
        response = urlopen(request, timeout=120)

        # Init
        params = {'method': 'initParam',
                  'courseID': self.course_id,
                  'userID': self.user_id}
        params = urllib.parse.urlencode(params).encode()
        request = Request(self.aicc_url, params, headers, method="POST")
        response = urlopen(request, timeout=120)
        #response = response.read()
        #items = self.find(self.section_ru, response)
        #sid = items[0][0]
        
        # Get lesson.xml
        url = (self.web_url + "lessionnew/gc/" + 
               self.course_name + "/lesson.xml")
        response = urlopen(url).read()
        lesson_title = self.find(self.lesson_title_ru, response, 'gb2312')[0]
        print("开始学习：%s" % lesson_title)
        items = self.find(self.stime_ru, response, 'gb2312')
        print("        本课程共%d节" % len(items))
        #print(items)
        #sid = ""

        #while sid:
        #    if items[0][0] == sid:
        #        break
        #    items.pop(0)

        headers = {
            'Accept': '*/*',
            #'Accept-Encoding': 'gzip, deflate',
            #'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            #'Content-Length': '48',
            'Content-Type': 'application/x-www-form-urlencoded',
            #'Host': 'jhce.jhxf.gov.cn',
            #'Origin': 'http://jhce.jhxf.gov.cn',
            'Referer': url,
            'User-Agent': self.user_agent
        }
                
        for item in items:         
            params = {'method': 'setParam',
                      'lastLocation': '0',
                      'SID': item[0],
                      'curtime': time.strftime('%Y-%m-%d %X', time.localtime()),
                      'STime': item[1],
                      'state': 'S',
                      'courseID': self.course_id,
                      'userID': self.user_id}
            params = urllib.parse.urlencode(params).encode()
            request = Request(self.aicc_url, params, headers, method="POST")
            response = urlopen(request, timeout=120).read()
            #if response:
            #    print(response.decode())
            
            self.progressbar(item[0][2:], int(item[1]))

            params = {'method': 'setParam',
                      'lastLocation': item[1]+'0000',
                      'SID': item[0],
                      'curtime': time.strftime('%Y-%m-%d %X', time.localtime()),
                      'STime': item[1],
                      'state': 'C',
                      'courseID': self.course_id,
                      'userID': self.user_id}
            params = urllib.parse.urlencode(params).encode()
            request = Request(self.aicc_url, params, headers, method="POST")
            #self.cj = copy.deepcopy(self.my_cj)
            response = urlopen(request, timeout=120).read()
            #if response:
            #    print(response.decode())
        
        print("课程学习结束")
        self.keep_clear = False

    def run(self): 
        self.cj.clear_session_cookies()
        self.login()
        while self.getcourses():
            self.playcourse()
            print("等待5秒后开始下一课...")
            time.sleep(5)
            self.cj.clear_session_cookies()
            self.login()


if __name__ == "__main__":
    a = AutoLearnOnline()
    a.run()
