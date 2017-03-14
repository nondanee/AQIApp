# -*- coding: utf-8 -*-

import StringIO, requests, re, base64, zlib, xmltodict
from io import BytesIO
from wcf.records import *
from wcf.xml2records import XMLParser
import MySQLdb
import datetime
import time

def getAllStationsData():
    #print action
    #print data
    output = StringIO.StringIO()
    output.write('<GetAllAQIPublishLive xmlns="http://tempuri.org/"></GetAllAQIPublishLive>')
    output.seek(0)

    r = XMLParser.parse(output)
    req = dump_records(r)

    r = requests.post(
        url='http://106.37.208.233:20035/ClientBin/Env-CnemcPublish-RiaServices-EnvCnemcPublishDomainService.svc/binary/GetAllAQIPublishLive',
        data=req,
        headers={'Content-Type': 'application/msbin1'})
    res = r.content

    buf = BytesIO(res)
    r = Record.parse(buf)

    print_records(r, fp=output)
    output.seek(0)

    pat = re.compile('<[^>]+>')
    enc = pat.sub('', output.readlines()[1][1:])[:-1]

    enc = base64.b64decode(enc)
    enc = zlib.decompress(enc)

    convertedDict = xmltodict.parse(enc)
    return convertedDict["ArrayOfAQIDataPublishLive"]["AQIDataPublishLive"]


def saveRawData():
    allData = getAllStationsData()
    
    conn=MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='?????',
    db='aircm',
    charset="utf8")
    
    cur=conn.cursor()
    
    updated = 0
    
    for i in xrange(0,len(allData)):

        TimePoint = datetime.datetime.strptime(allData[i]["TimePoint"],"%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M")

        StationCode = allData[i]["StationCode"]

        PositionName = allData[i]["PositionName"]

            
        if allData[i]["Longitude"]!=u'\u2014':
            Longitude = float(allData[i]["Longitude"])
        else:
            Longitude = None
            
        if allData[i]["Latitude"]!=u'\u2014':
            Latitude = float(allData[i]["Latitude"])
        else:
            Latitude = None
            

        Area = allData[i]["Area"]

        CityCode = int(allData[i]["CityCode"])

        ProvinceId = int(allData[i]["ProvinceId"])
        
        if allData[i]["AQI"]!=u'\u2014':
            AQI = int(allData[i]["AQI"])
        else:
            AQI = None

        if allData[i]["Quality"]!=u'\u2014':
            Quality = allData[i]["Quality"]
        else:
            Quality = None

            
        if allData[i]["O3"]!=u'\u2014':
            O3 = int(allData[i]["O3"])
        else:
            O3 = None
            
        if allData[i]["O3_24h"]!=u'\u2014':
            O3_24h = int(allData[i]["O3_24h"])
        else:
            O3_24h = None
            
        if allData[i]["O3_8h"]!=u'\u2014':
            O3_8h = int(allData[i]["O3_8h"])
        else:
            O3_8h = None
        
        if allData[i]["O3_8h_24h"]!=u'\u2014':
            O3_8h_24h = int(allData[i]["O3_8h_24h"])
        else:
            O3_8h_24h = None
        
        if allData[i]["CO"]!=u'\u2014':
            CO = float(allData[i]["CO"])
        else:
            CO = None
            
        if allData[i]["CO_24h"]!=u'\u2014':
            CO_24h = float(allData[i]["CO_24h"])
        else:
            CO_24h = None
            
        if allData[i]["SO2"]!=u'\u2014':
            SO2 = int(allData[i]["SO2"])
        else:
            SO2 = None
            
        if allData[i]["SO2_24h"]!=u'\u2014':
            SO2_24h = int(allData[i]["SO2_24h"])
        else:
            SO2_24h = None
            
        if allData[i]["NO2"]!=u'\u2014':
            NO2 = int(allData[i]["NO2"])
        else:
            NO2 = None
        
        if allData[i]["NO2_24h"]!=u'\u2014':
            NO2_24h = int(allData[i]["NO2_24h"])
        else:
            NO2_24h = None
            
        if allData[i]["PM2_5"]!=u'\u2014':
            PM2_5 = int(allData[i]["PM2_5"])
        else:
            PM2_5 = None
            
        if allData[i]["PM2_5_24h"]!=u'\u2014':
            PM2_5_24h = int(allData[i]["PM2_5_24h"])
        else:
            PM2_5_24h = None
            
        if allData[i]["PM10"]!=u'\u2014':
            PM10 = int(allData[i]["PM10"])
        else:
            PM10 = None
            
        if allData[i]["PM10_24h"]!=u'\u2014':
            PM10_24h = int(allData[i]["PM10_24h"])
        else:
            PM10_24h = None
        
        if allData[i]["PrimaryPollutant"]!=u'\u2014':
            PrimaryPollutant = allData[i]["PrimaryPollutant"]
        else:
            PrimaryPollutant = None
            
        if allData[i]["Unheathful"]!=u'\u2014':
            Unheathful = allData[i]["Unheathful"]
        else:
            Unheathful = None
            
        if allData[i]["Measure"]!=u'\u2014':
            Measure = allData[i]["Measure"]
        else:
            Measure = None
            
        if allData[i]["IsPublish"]==u"true":
            IsPublish = 1
        else:
            IsPublish = 0
            
        sql_judge='SELECT * FROM raw WHERE TimePoint="%s" AND StationCode="%s"'%(TimePoint, StationCode)
        judge=cur.execute(sql_judge)
        if judge!=0:
            continue
        updated = 1
        cur.execute('INSERT INTO raw VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(TimePoint, StationCode, PositionName, Longitude, Latitude, Area, CityCode, ProvinceId, AQI, Quality, O3, O3_24h, O3_8h, O3_8h_24h, CO, CO_24h, SO2, SO2_24h, NO2, NO2_24h, PM2_5, PM2_5_24h, PM10, PM10_24h, PrimaryPollutant, Unheathful, Measure, IsPublish))
        conn.commit()
        
    cur.close()
    conn.close()
    return updated

    
def processData():
    conn=MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='?????',
    db='aircm',
    charset="utf8")
    
    cur=conn.cursor()
    
    now=datetime.datetime.now()
    thisHour=now.strftime("%Y-%m-%d %H:00")
    lastHour=(now-datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:00")
    
    allCity=[u"北京市",u"天津市",u"石家庄市",u"唐山市",u"秦皇岛市",u"邯郸市",u"保定市",u"张家口市",u"承德市",u"廊坊市",u"沧州市",u"衡水市",u"邢台市",u"太原市",u"呼和浩特市",u"沈阳市",u"大连市",u"长春市",u"哈尔滨市",u"上海市",u"南京市",u"苏州市",u"南通市",u"连云港市",u"徐州市",u"扬州市",u"无锡市",u"常州市",u"镇江市",u"泰州市",u"淮安市",u"盐城市",u"宿迁市",u"杭州市",u"宁波市",u"温州市",u"绍兴市",u"湖州市",u"嘉兴市",u"台州市",u"舟山市",u"金华市",u"衢州市",u"丽水市",u"合肥市",u"福州市",u"厦门市",u"南昌市",u"济南市",u"青岛市",u"郑州市",u"武汉市",u"长沙市",u"广州市",u"深圳市",u"珠海市",u"佛山市",u"中山市",u"江门市",u"东莞市",u"惠州市",u"肇庆市",u"南宁市",u"海口市",u"重庆市",u"成都市",u"贵阳市",u"昆明市",u"拉萨市",u"西安市",u"兰州市",u"西宁市",u"银川市",u"乌鲁木齐市",u"湘潭市",u"株洲市",u"包头市",u"鄂尔多斯市",u"营口市",u"丹东市",u"盘锦市",u"葫芦岛市",u"泉州市",u"莱芜市",u"临沂市",u"德州市",u"聊城市",u"滨州市",u"淄博市",u"枣庄市",u"烟台市",u"潍坊市",u"济宁市",u"泰安市",u"日照市",u"威海市",u"东营市",u"韶关市",u"汕头市",u"湛江市",u"茂名市",u"梅州市",u"汕尾市",u"河源市",u"阳江市",u"清远市",u"潮州市",u"揭阳市",u"云浮市",u"玉溪市",u"菏泽市",u"大同市",u"长治市",u"临汾市",u"阳泉市",u"赤峰市",u"鞍山市",u"抚顺市",u"本溪市",u"锦州市",u"吉林市",u"齐齐哈尔市",u"牡丹江市",u"大庆市",u"芜湖市",u"马鞍山市",u"九江市",u"洛阳市",u"安阳市",u"开封市",u"焦作市",u"平顶山市",u"三门峡市",u"宜昌市",u"荆州市",u"岳阳市",u"常德市",u"张家界市",u"桂林市",u"北海市",u"柳州市",u"三亚市",u"绵阳市",u"宜宾市",u"攀枝花市",u"泸州市",u"自贡市",u"德阳市",u"南充市",u"遵义市",u"曲靖市",u"咸阳市",u"铜川市",u"延安市",u"宝鸡市",u"渭南市",u"金昌市",u"嘉峪关市",u"石嘴山市",u"克拉玛依市",u"库尔勒市",u"寿光市",u"章丘市",u"即墨市",u"胶南市",u"胶州市",u"莱西市",u"平度市",u"蓬莱市",u"招远市",u"莱州市",u"荣成市",u"文登市",u"乳山市",u"吴江市",u"昆山市",u"常熟市",u"张家港市",u"太仓市",u"句容市",u"江阴市",u"宜兴市",u"金坛市",u"溧阳市",u"海门市",u"临安市",u"富阳市",u"义乌市",u"瓦房店市",u"信阳市",u"周口市",u"漳州市",u"晋城市",u"朔州市",u"晋中市",u"运城市",u"忻州市",u"吕梁市",u"乌海市",u"通辽市",u"呼伦贝尔市",u"巴彦淖尔市",u"乌兰察布市",u"兴安盟",u"锡林郭勒盟",u"阿拉善盟",u"阜新市",u"辽阳市",u"铁岭市",u"朝阳市",u"四平市",u"辽源市",u"通化市",u"白山市",u"松原市",u"白城市",u"延边州",u"鸡西市",u"鹤岗市",u"双鸭山市",u"伊春市",u"佳木斯市",u"七台河市",u"黑河市",u"绥化市",u"大兴安岭地区",u"蚌埠市",u"淮南市",u"淮北市",u"铜陵市",u"安庆市",u"黄山市",u"滁州市",u"阜阳市",u"宿州市",u"六安市",u"亳州市",u"池州市",u"宣城市",u"莆田市",u"三明市",u"南平市",u"龙岩市",u"宁德市",u"景德镇市",u"萍乡市",u"新余市",u"鹰潭市",u"赣州市",u"吉安市",u"宜春市",u"抚州市",u"上饶市",u"鹤壁市",u"新乡市",u"濮阳市",u"许昌市",u"漯河市",u"南阳市",u"商丘市",u"驻马店市",u"黄石市",u"十堰市",u"襄阳市",u"鄂州市",u"荆门市",u"孝感市",u"黄冈市",u"咸宁市",u"随州市",u"恩施州",u"衡阳市",u"邵阳市",u"益阳市",u"郴州市",u"永州市",u"怀化市",u"娄底市",u"湘西州",u"梧州市",u"防城港市",u"钦州市",u"贵港市",u"玉林市",u"百色市",u"贺州市",u"河池市",u"来宾市",u"崇左市",u"广元市",u"遂宁市",u"内江市",u"乐山市",u"眉山市",u"广安市",u"达州市",u"雅安市",u"巴中市",u"资阳市",u"阿坝州",u"甘孜州",u"凉山州",u"六盘水市",u"安顺市",u"铜仁地区",u"毕节市",u"黔西南州",u"黔东南州",u"黔南州",u"保山市",u"昭通市",u"丽江市",u"普洱市",u"临沧市",u"楚雄州",u"红河州",u"文山州",u"西双版纳州",u"大理州",u"德宏州",u"怒江州",u"迪庆州",u"昌都地区",u"山南地区",u"日喀则地区",u"那曲地区",u"阿里地区",u"林芝地区",u"汉中市",u"榆林市",u"安康市",u"商洛市",u"白银市",u"天水市",u"武威市",u"张掖市",u"平凉市",u"酒泉市",u"庆阳市",u"定西市",u"陇南市",u"临夏州",u"甘南州",u"海东地区",u"海北州",u"黄南州",u"海南州",u"果洛州",u"玉树州",u"海西州",u"吴忠市",u"中卫市",u"固原市",u"吐鲁番地区",u"哈密地区",u"昌吉州",u"博州",u"阿克苏地区",u"克州",u"喀什地区",u"和田地区",u"伊犁哈萨克州",u"塔城地区",u"阿勒泰地区",u"石河子市",u"五家渠市",]

    for i in xrange(0,len(allCity)):
        
        sql_thishour='SELECT AVG(AQI), AVG(O3), AVG(O3_24h), AVG(O3_8h), AVG(O3_8h_24h), AVG(CO), AVG(CO_24h), AVG(SO2), AVG(SO2_24h), AVG(NO2), AVG(NO2_24h), AVG(PM2_5), AVG(PM2_5_24h), AVG(PM10), AVG(PM10_24h) FROM raw WHERE TimePoint="%s" AND Area="%s";'%(thisHour,allCity[i])

        cur.execute(sql_thishour)
        oneCitydata=cur.fetchall()

        if oneCitydata[0][0]!=None:
            AQI = int(round(oneCitydata[0][0]))
        else:
            AQI = None
        
        if oneCitydata[0][1]!=None:
            O3 = int(round(oneCitydata[0][1]))
        else:
            O3 = None
        
        if oneCitydata[0][2]!=None:
            O3_24h = int(round(oneCitydata[0][2]))
        else:
            O3_24h = None
        
        if oneCitydata[0][3]!=None:
            O3_8h = int(round(oneCitydata[0][3]))
        else:
            O3_8h = None
        
        if oneCitydata[0][4]!=None:
            O3_8h_24h = int(round(oneCitydata[0][4]))
        else:
            O3_8h_24h = None
        
        if oneCitydata[0][5]!=None:
            CO = round(float(oneCitydata[0][5])+0.00000002,1)
        else:
            CO = None
        
        if oneCitydata[0][6]!=None:
            CO_24h = round(float(oneCitydata[0][6])+0.00000002,1)
        else:
            CO_24h = None
        
        if oneCitydata[0][7]!=None:
            SO2 = int(round(oneCitydata[0][7]))
        else:
            SO2 = None
        
        if oneCitydata[0][8]!=None:
            SO2_24h = int(round(oneCitydata[0][8]))
        else:
            SO2_24h = None
        
        if oneCitydata[0][9]!=None:
            NO2 = int(round(oneCitydata[0][9]))
        else:
            NO2 = None
        
        if oneCitydata[0][10]!=None:
            NO2_24h = int(round(oneCitydata[0][10]))
        else:
            NO2_24h = None
        
        if oneCitydata[0][11]!=None:
            PM2_5 = int(round(oneCitydata[0][11]))
        else:
            PM2_5 = None     
        
        if oneCitydata[0][12]!=None:
            PM2_5_24h = int(round(oneCitydata[0][12]))
        else:
            PM2_5_24h = None
        
        if oneCitydata[0][13]!=None:
            PM10 = int(round(oneCitydata[0][13]))
        else:
            PM10 = None
            
        if oneCitydata[0][14]!=None:
            PM10_24 = int(round(oneCitydata[0][14]))
        else:
            PM10_24 = None
        
        City=re.sub(u'[市|地区]',"",allCity[i])

        sql_lasthour='SELECT AQI FROM working WHERE TimePoint="%s" and City="%s";'%(lastHour,City)   
        cur.execute(sql_lasthour)
        lastHourData=cur.fetchall()
        
        AQI_lasthour=lastHourData[0][0]
        
        if AQI_lasthour!=AQI:
            if AQI_lasthour>AQI:
                Trend=-1
            else:
                Trend=1
        else:
            Trend=0

        if AQI_lasthour==None or AQI==None:
            Trend=None
        
        sql_try='SELECT * FROM working WHERE TimePoint="%s" AND City="%s"'%(thisHour, City)
        judge=cur.execute(sql_try)
        if judge!=0:
            continue
        
        cur.execute('INSERT INTO working VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(thisHour,City,AQI,Trend,O3,O3_24h,O3_8h,O3_8h_24h,CO ,CO_24h,SO2,SO2_24h,NO2,NO2_24h,PM2_5 ,PM2_5_24h,PM10,PM10_24))
        conn.commit()
        
    cur.close()
    conn.close()

runtime=datetime.datetime.now()
if runtime.minute<=35 and runtime.minute>=20:
    updated=saveRawData()
    if updated==1:
        processData()
