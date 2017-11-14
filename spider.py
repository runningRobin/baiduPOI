# -*- coding:utf-8 -*-
import json
import os
import requests
import time


class BaiDuPOI(object):
    def __init__(self, itemy, loc):
        self.itemy = itemy
        self.loc = loc

    def urls(self):
        api_key = 'IU2iDn2umGU3mq2uSERfZ6NzAVwcFSHw'
        urls = []
        for pages in range(0, 20):
            url = 'http://api.map.baidu.com/place/v2/search?query=' + self.itemy + '&bounds=' + self.loc + '&page_size=20&page_num=' + str(
                pages) + '&output=json&ak=' + api_key
            urls.append(url)
        return urls

    def baidu_search(self):
        json_sel = []
        for url in self.urls():
            data = requests.get(url).json()
            try:
                for item in data['results']:
                    jname = item["name"]
                    jlat = item["location"]["lat"]
                    jlng = item["location"]["lng"]
                    js_sel = jname + ',' + str(jlat) + ',' + str(jlng)
                    json_sel.append(js_sel)
                return json_sel
            except Exception as e:
                print(e)


class LocaDiv(object):
    def __init__(self, loc_all):
        self.loc_all = loc_all

    def lat_all(self):
        lat_sw = float(self.loc_all.split(',')[0])
        lat_ne = float(self.loc_all.split(',')[2])
        lat_list = []
        for i in range(0, int((lat_ne - lat_sw + 0.0001) / 0.05)):
            lat_list.append(lat_sw + 0.05 * i)
        lat_list.append(lat_ne)
        return lat_list

    def lng_all(self):
        lng_sw = float(self.loc_all.split(',')[1])
        lng_ne = float(self.loc_all.split(',')[3])
        lng_list = []
        for i in range(0, int((lng_ne - lng_sw + 0.0001) / 0.05)):
            lng_list.append(lng_sw + 0.05 * i)
        lng_list.append(lng_ne)
        return lng_list

    def ls_com(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ab_list = []
        for i in range(0, len(l1)):
            a = str(l1[i])
            for i2 in range(0, len(l2)):
                b = str(l2[i2])
                ab = a + ',' + b
                ab_list.append(ab)
        return ab_list

    def ls_row(self):
        l1 = self.lat_all()
        l2 = self.lng_all()
        ls_com_v = self.ls_com()
        ls = []
        for n in range(0, len(l1) - 1):
            for i in range(0 + (len(l1) + 1) * n, len(l2) + (len(l2)) * n - 1):
                a = ls_com_v[i]
                b = ls_com_v[i + len(l2) + 1]
                ab = a + ',' + b
                ls.append(ab)
        return ls


if __name__ == '__main__':
    baidu_api = 'wGNyxOAXHYwHW4k67AACUWhX'  # 这里填入你的百度API
    print("开始爬数据，请稍等...")
    start_time = time.time()
    loc = LocaDiv('31.261,120.552,31.386,120.761')
    # 120.552244,31.261114    120.760938,31.385985
    locs_to_use = loc.ls_row()
    for loc_to_use in locs_to_use:
        par = BaiDuPOI(u'宾馆', loc_to_use)  # 请修改这里的参数
        a = par.baidu_search()
        doc = open('baidu_csv.csv', 'a', encoding='utf-8')
        for ax in a:
            doc.write(ax)
            doc.write('\n')
        doc.close
    end_time = time.time()
    print("数据爬取完毕，用时%.2f秒" % (end_time - start_time))