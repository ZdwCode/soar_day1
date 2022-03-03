import pandas as pd;
import requests
from bs4 import  BeautifulSoup;

df=pd.read_excel('logo.xlsx')
df['logo_url']=''
df['type']=0;

headers={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
}
for i in range(len(df)):
    name=df.loc[i][0]
    url=df.loc[i][1]

    #测试 ：
    #url='https://www.aleyole.com/' #使用自动化工具
    #url='https://www.barrie.com/en/' 需要验证
    #url='https://www.paulandshark.com/'
    #url='https://www.lardini.com/us_en/'
    #print(f"开始爬取网页{url}了")

    try:
        response = requests.get(url,headers=headers)
        response.encoding='utf-8';

        #print(response.text)

        #先处理img
        page=BeautifulSoup(response.text,'html.parser');
        imgs=page.findAll('img');
        # print(type(imgs));
        # print(len(imgs))
        # print(f'img为{imgs}')
        # if len(imgs) ==0 :
        #     print('没匹配到')

        flag=0; # 表示没有找到logo
        logos = [] # 保存logo的url

        for img in imgs:
            src=img.get('src');
            content = ''

            # if "logo" in str(img) or "Logo" in str(img):
            #     content=src;


            if src is not None:#有些img中没有src标签直接跳过
                if "logo" in src or "Logo" in src:
                    if src.startswith('//'):
                        content = 'https:' + src
                    elif src.startswith('/'):
                        if url.endswith('/'):
                            content = url[0:-1] + src
                        else:
                            content = url + content
                    else:#不需要拼接
                        content = src
            #稍后封装成方法

            data_src = img.get('data-srcset');
            if data_src is not None:#有些img中没有src标签直接跳过
                if "logo" in data_src or "Logo" in data_src:
                    if data_src.startswith('//'):
                        content = 'https:' + data_src
                    elif data_src.startswith('/'):
                        if url.endswith('/'):
                            content = url[0:-1] + data_src
                        else:
                            content = url + content
                    else:#不需要拼接
                        content = data_src

            if content != '':#至少匹配到了一个带有logo的url
                logos.append(content)
                flag=1;

            # http://jogunshop.img18.kr/web/intop/pc/main_logo.png`

        if flag == 1: #找到了logo
            #首先对logos去重 采用set集合去重
            logos = list(set(logos))

            #测试打印：
            print(i,url)
            print(logos)
            df['type'].loc[i] = 1;
            df['logo_url'].loc[i]=str(logos)
        elif flag ==0:#如果此时整个content都没有--说明页面没有img的logo而是svg了
            '''需要找svg的页面'''
            print(i,url,'没有找到logo但svg如下')

    except Exception as e:
        #print(e);
        print(f"{i} 网页{url}出错,response{response}");
        print("错误信息如下",e)
    #获取标签
    print('------------------------')
#print(df.shape)
df.to_excel('1.xlsx')

