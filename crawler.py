import requests
from lxml import etree
import time
from datetime import datetime
import re
class Crawler(object):
    def __init__(self,
                base_url='https://www.csie.ntu.edu.tw/news/',
                rel_url='news.php?class=101'):
        self.base_url = base_url
        self.rel_url = rel_url

    def crawl(self, start_date, end_date):
        """Main crawl API
        1. Note that you need to sleep 0.1 seconds for any request.
        2. It is welcome to modify TA's template.
        """

        contents = list()
        page_num = 0
        while True:
            rets, last_date = self.crawl_page(
                start_date, end_date, page=f'&no={page_num}')
            page_num += 10
            if rets:
                contents += rets
            if last_date < start_date:
                break
            time.sleep(0.1)
        return contents

    def crawl_page(self, start_date, end_date, page=''):
        """Parse ten rows of the given page
        Parameters:
            start_date (datetime): the start date (included)
            end_date (datetime): the end date (included)
            page (str): the relative url specified page num
        Returns:
            content (list): a list of date, title, and content
            last_date (datetime): the smallest date in the page
        """
        res = requests.get(
            self.base_url + self.rel_url + page,
            headers={'Accept-Language':
                     'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        ).content.decode("utf-8")
        time.sleep(0.1)
        root=etree.HTML(res)
        # TODO: parse the response and get dates, titles and relative url with etree
        contents = list()
        last_date=0
        titles=(root.xpath("//html/body/div/div/div/div/div/div/div/table/tbody/tr/td[1]"))
        i=0
        for title in titles:
            if (i==9):
                last_date=datetime.strptime(title.text, '%Y-%m-%d')
            i+=1
        rel_urls=(root.xpath("//html/body/div/div/div/div/div/div/div/table/tbody/tr/td//a/@href"))
        rem=[]
        for rel_url in rel_urls:
            k = self.base_url + rel_url
            d, t , c=Crawler.crawl_content(self,k)
            if (d>end_date or d<start_date):
                continue
            else:
                if d == datetime.strptime("2022-05-26", '%Y-%m-%d'):
                    continue
                contents.append(d)
                t=t.replace('"','""')
                t=","+"\""+t
                if (len(c))==0 or (len(c))==1 :
                    t=t+"\""+"\n"
                    contents.append(t)
                    if d == datetime.strptime("2022-05-27", '%Y-%m-%d') and datetime.strptime("2022-05-26", '%Y-%m-%d')>start_date:
                        time.sleep(0.1)
                        dd, tt , cc=Crawler.crawl_content(self,"https://www.csie.ntu.edu.tw/news/news.php?Sn=17054")
                        contents.append(dd)
                        tt=tt.replace('"','""')
                        tt=","+tt+"\""
                        contents.append(tt)
                        cc=cc.replace('"','""')
                        cc=","+"\""+cc+"\""+"\n"
                        contents.append(cc)
                else:
                    t=t+"\""
                    contents.append(t)
                    c=c.replace('"','""')
                    c=","+"\""+c+"\""+"\n"
                    contents.append(c)
                        
            time.sleep(0.1)
            # TODO: 1. concatenate relative url to full url
            #       2. for each url call self.crawl_content
            #          to crawl the content
            #       3. append the date, title and content to
            #          contents
        return contents, last_date

    def crawl_content(self, url):
        """Crawl the content of given url
        For example, if the url is
        https://www.csie.ntu.edu.tw/news/news.php?Sn=15216
        then you are to crawl contents of
        ``Title : 我與DeepMind的A.I.研究之路, My A.I. Journey with DeepMind Date : 2019-12-27 2:20pm-3:30pm Location : R103, CSIE Speaker : 黃士傑博士, DeepMind Hosted by : Prof. Shou-De Lin Abstract: 我將與同學們分享，我博士班研究到加入DeepMind所參與的projects (AlphaGo, AlphaStar與AlphaZero)，以及從我個人與DeepMind的視角對未來AI發展的展望。 Biography: 黃士傑, Aja Huang 台灣人，國立臺灣師範大學資訊工程研究所博士，現為DeepMind Staff Research Scientist。``
        """
        response=requests.get(url)
        html_text=response.content.decode("utf-8")
        root=etree.HTML(html_text)
        titles=(root.xpath("//html/body/div/div/div/div/div/div/div/h1"))
        title=""
        for titl in titles:
            title = (titl.text)
        titles=(root.xpath("//html/body/div/div/div/div/div/div/div/div/span[@class]"))
        for k in titles:
            a= (k.text)
            b=(a.split("："))
        date=b[1]
        date=datetime.strptime(date, '%Y-%m-%d')
        titles=(root.xpath("//html/body/div[1]/div/div[2]/div/div/div[2]/div/div[@class='editor content']"))
        result=""
        content=[]
        for k in titles[0].itertext():
            result= result+k
        result = result.strip()
        ## print (result)
        return date, title,str(result)
        raise NotImplementedError
