# 导入模块
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq
import pandas as pd  # 保存为Excel文件
import time
start = time.clock()


class DoctorData(object):       # 爬取微医网医生数据类
    # 初始化应该具有的属性
    def __init__(self):
        self._datafile = list()

    async def main(self, num):          # 爬取网页数据

        try:
            browser = await launch(headless=True)
            page = await browser.newPage()

            print(f"正在爬取第 {num} 页")
            await page.goto("https://www.guahao.com/expert/all/全国/all/不限/p{}".format(num))
            content = await page.content()
            await browser.close()
            self.parser_html(content)
            print("获取成功")
            print("存取数据中....")

            data = pd.DataFrame(self._datafile)
            data.to_excel("微医全国医生数据.xls", encoding='utf-8')     # 导出数据为Excel
            end = time.clock()
            print("存储完成! 用时：", end - start, 's')
        except Exception as e:
            print(e.args)
        finally:
            num += 1
            await self.main(num)

    def parser_html(self, html_content):        # 网页内容解析

        doc = pq(html_content)
        items = doc(".g-doctor-item").items()
        for item in items:
            name_title = item.find(".g-doc-baseinfo>dl>dt").text()                      # 姓名和级别
            department = item.find(".g-doc-baseinfo>dl>dd>p:eq(0)").text()              # 科室
            address = item.find(".g-doc-baseinfo>dl>dd>p:eq(1)").text()                 # 医院地址
            score = item.find(".star-count em").text()                                  # 评分
            visit = item.find(".star-count i").text()                                   # 问诊量
            expert_team = item.find(".expert-team").text()                              # 专家团队
            service_price_img_text = item.find(".service-name:eq(0)>.fee").text()       # 图文问诊
            service_price_lip_read = item.find(".service-name:eq(1)>.fee").text()       # 视话问诊

            doctor_datafile = {
                "姓名": name_title.split(" ")[0],
                "医生职称": name_title.split(" ")[1],
                "所处科室": department,
                "所在医院": address,
                "评分": score,
                "问诊量": visit,
                "专家团队成员": expert_team,
                "图文问诊价格": service_price_img_text,
                "视话问诊价格": service_price_lip_read
            }

            self._datafile.append(doctor_datafile)

    def run(self):      # 项目启动
        loop = asyncio.get_event_loop()
        task = asyncio.get_event_loop().run_until_complete(self.main(1))        # 异步
        loop.run_until_complete(task)


if __name__ == '__main__':
    doctor = DoctorData()
    doctor.run()
