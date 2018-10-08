import requests
import json
from station import stations
import prettytable
class Traininfo:
    def __init__(self):
        self.data = []
        self.date=''
        url=self.getUrl()
        self.data=self.getData(url)
        self.Print()

    def getUrl(self):
        startflag = False
        endflag = False
        while startflag == False:
            start = input("请输入始发地：\n")
            startflag = stations.__contains__(start)
            if startflag == False:
                print('始发地输入错误！')
        while endflag == False:
            end = input("请输入目的地：\n")
            endflag = stations.__contains__(end)
            if endflag == False:
                print('目的地输入错误！')

        self.date = input("请输入日期(格式为xxxx-xx-xx)：\n")

        url = 'https://kyfw.12306.cn/otn/leftTicket/queryA?leftTicketDTO.train_date=' \
              + self.date + '&leftTicketDTO.from_station=' \
              + stations[start] + '&leftTicketDTO.to_station=' \
              + stations[end] + '&purpose_codes=ADULT'
        return url

    def getData(self,url):
        dataweb = requests.get(url)
        datajson = json.loads(dataweb.text)
        datatrains = datajson['data']['result']
        restations=datajson['data']['map']#地点缩写：地点全称的字典
        dataans = []
        for train in datatrains:
            per = {
                'train_no': '',
                'from_station_no': '',
                'to_station_no': '',
                'seat_types': '',
                'chufazhan':'',
                'dadaozhan':'',
                'checi': '',
                'chufasj': '',
                'didasj': '',
                'lishi': '',
                'erdeng': '',
                'yideng': '',
                'shangwu': '',
                'wuzuo':''
            }
            train = train.split('|')
            per['train_no'] = train[2]
            per['from_station_no'] = train[16]
            per['to_station_no'] = train[17]
            per['seat_types'] = train[35]
            per['chufazhan']=train[6]
            per['dadaozhan']=train[7]

            #将得到站点名字由缩写转换全称
            per['chufazhan']=restations[per['chufazhan']]
            per['dadaozhan']=restations[per['dadaozhan']]

            per['checi'] = train[3]
            per['chufasj'] = train[8]
            per['didasj'] = train[9]
            per['lishi'] = train[10]
            per['erdeng'] = train[30]
            per['yideng'] = train[31]
            per['shangwu'] = train[32]
            per['wuzuo']=train[26]
            for value in per:
                if (per[value] == ''):
                    per[value] = '-'
            dataans.append(per)
        return dataans

    def Print(self):
        price={
            'shangwu':'',
            'yideng':'',
            'erdeng':'',
            'wuzuo':'',
        }
        table = prettytable.PrettyTable()
        table.field_names = ["车次","出发站","达到站" ,"出发时间", "抵达时间", "历时", "二等座", "一等座", "商务座","无座"]
        for per in self.data:
            price=self.GetPrice(per['train_no'],per['from_station_no'],per['to_station_no'],per['seat_types'],self.date,price)
            table.add_row([per['checi'],per['chufazhan'],per['dadaozhan'], per['chufasj'], per['didasj'], per['lishi'], per['erdeng']+'\n'+price['erdeng'], per['yideng']+'\n'+price['yideng'],
                           per['shangwu']+'\n'+price['shangwu'],per['wuzuo']+'\n'+price['wuzuo']])
        print(table)

    def GetPrice(self,train_no,from_station_no,to_station_no,seat_types,date,price):
        url = 'https://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=' \
              + train_no + '&from_station_no=' \
              + from_station_no + '&to_station_no=' \
              + to_station_no + '&seat_types=' \
              + seat_types + '&train_date=' + date
        priceweb=requests.get(url)
        pricejson=json.loads(priceweb.text)
        pricedata=pricejson['data']
        shangwu=pricedata.__contains__('A9')#商务
        yideng=pricedata.__contains__('M')#一等
        erdeng=pricedata.__contains__('O')#二等
        wuzuo=pricedata.__contains__('WZ')#无座
        if shangwu:
            price['shangwu']=pricedata['A9']
        else :
            price['shangwu']=''
        if yideng:
            price['yideng']=pricedata['M']
        else :
            price['yideng']=''
        if erdeng:
            price['erdeng']=pricedata['O']
        else :
            price['erdeng']=''
        if wuzuo:
            price['wuzuo']=pricedata['WZ']
        else :
            price['wuzuo']=''
        return price


message=Traininfo()
