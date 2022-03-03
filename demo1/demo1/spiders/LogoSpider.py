import scrapy
import pandas as pd;
from bs4 import BeautifulSoup
class LogospiderSpider(scrapy.Spider):
    name = 'LogoSpider'
    allowed_domains = ['test.com']
    start_urls = []

    def __init__(self):
        scrapy.Spider.__init__(self)
        df = pd.read_excel('logo.xlsx');

        #加两个等级，方便我们减少不必要的循环
        df['logo_url'] = '';
        df['type'] = 0;

        self.data=df;
        self.data_len=len(df)

        # 保存一下请求的url和域名 稍后会拼接
        self.url=''
        self.domain=''


    #重写父类start_requests() 方便动态定义start_urls
    def start_requests(self):
        # 配置url
        for i in range(self.data_len):

            self.domain = self.data.loc[i][0]# 域名
            self.url = self.data.loc[i][1]# url
            self.start_urls.append(self.url)

        for url in self.start_urls:
            yield scrapy.Request(url, dont_filter=True)

    def parse(self, response):
        LogospiderSpider.getLogo_by_img(response,self.url)
        pass

    @staticmethod
    def getLogo_by_img(self,response,url):
        try:
            response.encoding = 'utf-8';
            #匹配img标签
            page = BeautifulSoup(response.text, 'html.parser');
            imgs = page.findAll('img');

            flag = 0  # 表示没有找到logo
            logos = []  # 保存logo的url

            for img in imgs:
                src = img.get('src');
                content = ''
                if src is not None:  # 有些img中没有src标签直接跳过
                    if "logo" in src or "Logo" in src:
                        if src.startswith('//'):
                            content = 'https:' + src
                        elif src.startswith('/'):
                            if url.endswith('/'):
                                content = url[0:-1] + src
                            else:
                                content = url + content
                        else:  # 不需要拼接
                            content = src

                # 这里应该封装成静态方法

                data_src = img.get('data-srcset');
                if data_src is not None:  # 有些img中没有src标签直接跳过
                    if "logo" in data_src or "Logo" in data_src:
                        if data_src.startswith('//'):
                            content = 'https:' + data_src
                        elif data_src.startswith('/'):
                            if url.endswith('/'):
                                content = url[0:-1] + data_src
                            else:
                                content = url + content
                        else:  # 不需要拼接
                            content = data_src

                if content != '':  # 至少匹配到了一个带有logo的url
                    logos.append(content)
                    flag = 1;


            if flag == 1:  # 找到了logo
                # 首先对logos去重 采用set集合去重
                logos = list(set(logos))

        except Exception as e:
            # print(e);
            print(f"网页{url}出错,response{response}");
            print("错误信息如下", e)

    def getLogo_by_svg(self):
        pass;


