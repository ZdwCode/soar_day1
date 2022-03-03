import scrapy
import csv


class DomainSpider(scrapy.Spider):
    name = 'domain'
    allowed_domains = ['domain.com']
    index=0
    #1是页面参数，可以考虑修改
    start_urls=['https://myip.ms/browse/sites/1/ownerID/376714/ownerIDii/376714/sort/6#sites_tbl_top',
                'https://myip.ms/browse/sites/1/ipID/23.227.38.32/ipIDii/23.227.38.32',
                'https://myip.ms/browse/sites/1/ipID/23.227.38.0/ipIDii/23.227.38.255']


    def parse(self, response):
        filename = 'item' + str(DomainSpider.index)+'.xlsx';
        f = open(filename, mode='w', encoding='utf-8');
        CSVwriter = csv.writer(f)
        DomainSpider.index+=1;
        url_header = DomainSpider.start_urls[0].split('/browse')[0]
        domains = response.xpath('//*[@id="sites_tbl"]/tbody/tr/td[@class="row_name"]/a/text()').extract()
        urls = response.xpath('//*[@id="sites_tbl"]/tbody/tr/td[@class="row_name"]/a/@href').extract()


        for domain, url in zip(domains, urls):
            url = url_header + url
            dic={'demain':domain,'url':url}
            print(dic.values(),"++++++++++++")
            CSVwriter.writerow(dic.values(),)



