import requests
from bs4 import BeautifulSoup
import msvcrt


def pwd_input():
    """输入密码替换为星号
    :return: 字符串形式密码
    """
    chars = []
    while True:
        try:
            new_char = msvcrt.getch().decode(encoding="utf-8")
        except:
            return input("你很可能不是在cmd命令行下运行，密码输入将不能隐藏(〜￣△￣)〜:\n")
        if new_char in '\r\n':  # 如果是换行，则输入结束
            break
        elif new_char == '\b':  # 如果是退格，则删除密码末尾一位并且删除一个星号
            if chars:
                del chars[-1]
                msvcrt.putch('\b'.encode(encoding='utf-8'))  # 光标回退一格
                msvcrt.putch(' '.encode(encoding='utf-8'))  # 输出一个空格覆盖原来的星号
                msvcrt.putch('\b'.encode(encoding='utf-8'))  # 光标回退一格准备接受新的输入
        else:
            chars.append(new_char)
            msvcrt.putch('*'.encode(encoding='utf-8'))  # 显示为星号
    print('')
    return ''.join(chars)


def get_score_by_type(headers, cookies):
    # 构造一个列表，用来存放查询成绩的类型
    score_urls = ["http://newjw.cduestc.cn/gradeLnAllAction.do?type=ln&oper=qbinfo",
                  "http://newjw.cduestc.cn/gradeLnAllAction.do?type=ln&oper=sxinfo",
                  "http://newjw.cduestc.cn/gradeLnAllAction.do?type=ln&oper=fainfo",
                  "http://newjw.cduestc.cn/gradeLnAllAction.do?type=ln&oper=bjg"]
    choice = input("请输入你要进行的查询类型：\n1、全部及格成绩查询\n2、按课程属性成绩查询\n3、按方案成绩查询\n4、不及格成绩查询\n")
    while int(choice) not in range(0, 5):
        print("你的输入有误，请重新输入！")
        choice = input("请输入你要进行的查询类型：\n1、全部及格成绩查询\n2、按课程属性成绩查询\n3、按方案成绩查询\n4、不及格成绩查询\n")
    pass_score_url = score_urls[int(choice) - 1]
    pass_score_html = requests.get(pass_score_url, headers=headers, cookies=cookies, timeout=30)
    pass_score_html_content = pass_score_html.text
    # print(pass_score_html_content)
    # print(pass_score_html.status_code)
    # 将得到的教务系统的源码转换成BeautifulSoup对象，并指定解析器为lxml
    soup = BeautifulSoup(pass_score_html_content, "lxml")
    # 通过css选择器选出要用的数据
    # score_types = soup.select("td > b")
    # print(score_types)
    score_title = soup.select("#user > thead > tr")
    score_tables = soup.select("#user > tr")
    if len(score_tables) > 0:
        print(score_title[0].get_text(" | ", strip=True))
        for score in score_tables:
            print(score.get_text(" | ", strip=True))
        print("及格科目共计%s科" % len(score_tables))
    else:
        print("获取成绩失败，请检查你输入的学号或密码是否正确，网络连接是否正常！")
    holdon = input("你有两个选择：\n1、如需继续查询当前用户成绩请输入c\n2、如需查询其他用户成绩请输入b\n按其他任意键退出···\n")
    if holdon == "c":
        get_score_by_type(headers, cookies)
    if holdon == "b":
        get_scores()


def get_scores():
    try:
        # 请求教务系统首页
        hosturl = "http://newjw.cduestc.cn/"
        req = requests.get(hosturl, timeout=30)
        cookies = req.cookies
        # print(req.cookies)
        # 登录教务系统的url
        url = "http://newjw.cduestc.cn/loginAction.do"

        # 构造header
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                   "Accept-Encoding": "gzip, deflate, sdch",
                   "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4",
                   "Connection": "keep-alive",
                   'Cache-Control': "max-age=0",
                   "Host": "newjw.cduestc.cn",
                   "Upgrade-Insecure-Requests": "1",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/56.0.2924.87 Safari/537.36"
                   }
        # 构造request请求体数据
        zjh = input("请输入你的学号：\n").strip()
        print("请输入你的密码：")
        mm = pwd_input().strip()
        post_data = {"zjh": zjh, "mm": mm}
        # 发送请求进行登录
        html_content = requests.post(url, headers=headers, data=post_data, cookies=cookies, timeout=30)
        # print(html_content.text)
        get_score_by_type(headers, cookies)
        # holdon = input("你有两个选择：\n1、如需继续查询当前用户成绩请输入c\n2、如需查询其他用户成绩请输入b\n按其他任意键退出···\n")
        # if holdon == "c":
        #     get_score_by_type(headers, cookies)
        # if holdon == "b":
        #     get_scores()
    except:
        print("获取成绩失败，请检查你输入的学号或密码是否正确，网络连接是否正常！")
        holdon = input("如需继续查询成绩请输入c\n按其他任意键退出···\n")
        if holdon == "c":
            get_scores()

get_scores()
