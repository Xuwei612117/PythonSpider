import xlwt
import xlrd
import time
import requests
import threading
from lxml.html import etree
from xlutils.copy import copy
from concurrent.futures import ThreadPoolExecutor


class DoctorSpider(object):
    # 初始化应有的属性
    def __init__(self):
        wb = xlwt.Workbook()
        wb.add_sheet('全国医生详细数据')
        wb.save('微医医生数据表.xls')
        workbook1 = xlrd.open_workbook('微医医生数据表.xls', encoding_override='utf-8')
        new_workbook = copy(workbook1)
        new_worksheet = new_workbook.get_sheet(0)
        new_worksheet.write(0, 0, '姓名')
        new_worksheet.write(0, 1, '职称')
        new_worksheet.write(0, 2, '科室')
        new_worksheet.write(0, 3, '医院')
        new_worksheet.write(0, 4, '擅长')
        new_worksheet.write(0, 5, '评分')
        new_worksheet.write(0, 6, '问诊量')
        new_worksheet.write(0, 7, '图文问诊价格')
        new_worksheet.write(0, 8, '视频问诊价格')
        new_workbook.save("微医医生数据表.xls")
        self.url = 'https://www.guahao.com/expert/all/%E5%85%A8%E5%9B%BD/all/%E4%B8%8D%E9%99%90/p{}'
        print('表格创建完毕')

    def start(self, number):
        print('正在发起请求')
        response = requests.get(self.url.format(number))    # 得到结果response
        html = etree.HTML(response.content.decode())        # 转为xpath解析
        name1 = html.xpath('//*[@id="g-cfg"]/div[1]/div[2]/ul/li/div/dl/dt/a/text()')       # 提取姓名字段
        name = []
        for i in name1:
            if len(i) > 1:
                name.append(i)
        title = []
        title1 = html.xpath('//*[@id="g-cfg"]/div[1]/div[2]/ul/li/div/dl/dt/text()')        # 提取职称字段
        for i in title1:
            if "师" in i:
                title.append(i)
        department = html.xpath('//*[@id="g-cfg"]/div[1]/div[2]/ul/li/div/dl/dd/p[1]/text()')       # 提取科室字段，返回为列表
        hospital = html.xpath('//*[@id="g-cfg"]/div[1]/div[2]/ul/li/div/dl/dd/p[2]/span[1]/text()')     # 医院
        skill = html.xpath('//*[@id="g-cfg"]/div[1]/div[2]/ul/li/div[2]/div[1]/p/text()')           # 擅长
        score = html.xpath('//*[@id="g-cfg"]/div[1]/div[2]/ul/li/div[1]/dl/dd/p[3]/span[1]/em/text() | //*[@id="g-cfg"]/div[1]/div[2]/ul/li/div[1]/dl/dd/p[3]/span[1]/text()')      # 评分
        value = html.xpath('//*[@id="g-cfg"]/div[1]/div[2]/ul/li/div[1]/dl/dd/p[3]/span[2]/i/text()')   # 问诊量
        pic = html.xpath('//*[@id="g-cfg"]/div[1]/div[2]/ul/li/div[2]/div[2]/a[1]/span/em[2]/text()')   # 图文问诊
        vid = html.xpath('//*[@id="g-cfg"]/div[1]/div[2]/ul/li/div[2]/div[2]/a[2]/span/em[2]/text()')   # 视话问诊
        self.save(name, title, department, hospital, skill, score, value, pic, vid)

    def save(self, name, title, department, hospital, skill, score, value, pic, vid):       # 用save方法写入表格
        lock.acquire()      # acquire()方法提供了确定对象被锁定的标志
        print('正在写入表格')
        for i in range(len(name)):
            print(name[i])
            workbook = xlrd.open_workbook("微医医生数据表.xls", encoding_override="utf-8")     # 打开表格
            sheets = workbook.sheet_names()
            worksheet = workbook.sheet_by_name(sheets[0])
            rows_old = worksheet.nrows      # 获取当前行数
            new_workbook = copy(workbook)
            new_worksheet = new_workbook.get_sheet(0)
            new_worksheet.write(rows_old, 0, name[i].strip().replace(' ', ''))
            new_worksheet.write(rows_old, 1, title[i].strip().replace(' ', ''))
            new_worksheet.write(rows_old, 2, department[i].strip().replace(' ', ''))
            new_worksheet.write(rows_old, 3, hospital[i].strip().replace(' ', ''))
            new_worksheet.write(rows_old, 4, skill[i].strip().replace(' ', ''))
            new_worksheet.write(rows_old, 5, score[i].strip().replace(' ', ''))
            new_worksheet.write(rows_old, 6, value[i].strip().replace(' ', ''))
            new_worksheet.write(rows_old, 7, pic[i].strip().replace(' ', ''))
            new_worksheet.write(rows_old, 8, vid[i].strip().replace(' ', ''))
            new_workbook.save("微医医生数据表.xls")
            lock.release()      # release()在对象被当前线程使用完毕后将当前对象释放
            time.sleep(5)
            print('写入完毕')


if __name__ == '__main__':
    sp = DoctorSpider()
    lock = threading.Lock()     # 加速
    pool = ThreadPoolExecutor(20)
    for page_nums in range(1, 39):
        pool.submit(sp.start, page_nums)
        sp.start(page_nums)
