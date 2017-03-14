# -*- encoding=utf-8 -*- 

import logging
import asyncio
import aiohttp
import aiomysql
import re
import json
import datetime
import collections
from aiohttp import web

logging.basicConfig(level='INFO')
logger = logging.getLogger('RUNNING')

def valuecheck(wait2check):

    Citydict={u'七台河':u'City="七台河"',u'三亚':u'City="三亚"',u'三明':u'City="三明"',u'三门峡':u'City="三门峡"',u'上海':u'City="上海"',u'上饶':u'City="上饶"',u'东莞':u'City="东莞"',u'东营':u'City="东营"',u'中卫':u'City="中卫"',u'中山':u'City="中山"',u'临夏州':u'City="临夏州"',u'临安':u'City="临安"',u'临汾':u'City="临汾"',u'临沂':u'City="临沂"',u'临沧':u'City="临沧"',u'丹东':u'City="丹东"',u'丽水':u'City="丽水"',u'丽江':u'City="丽江"',u'义乌':u'City="义乌"',u'乌兰察布':u'City="乌兰察布"',u'乌海':u'City="乌海"',u'乌鲁木齐':u'City="乌鲁木齐"',u'乐山':u'City="乐山"',u'九江':u'City="九江"',u'乳山':u'City="乳山"',u'云浮':u'City="云浮"',u'五家渠':u'City="五家渠"',u'亳州':u'City="亳州"',u'伊春':u'City="伊春"',u'伊犁哈萨克州':u'City="伊犁哈萨克州"',u'佛山':u'City="佛山"',u'佳木斯':u'City="佳木斯"',u'保定':u'City="保定"',u'保山':u'City="保山"',u'信阳':u'City="信阳"',u'克州':u'City="克州"',u'克拉玛依':u'City="克拉玛依"',u'六安':u'City="六安"',u'六盘水':u'City="六盘水"',u'兰州':u'City="兰州"',u'兴安盟':u'City="兴安盟"',u'内江':u'City="内江"',u'凉山州':u'City="凉山州"',u'包头':u'City="包头"',u'北京':u'City="北京"',u'北海':u'City="北海"',u'十堰':u'City="十堰"',u'南京':u'City="南京"',u'南充':u'City="南充"',u'南宁':u'City="南宁"',u'南平':u'City="南平"',u'南昌':u'City="南昌"',u'南通':u'City="南通"',u'南阳':u'City="南阳"',u'博州':u'City="博州"',u'即墨':u'City="即墨"',u'厦门':u'City="厦门"',u'双鸭山':u'City="双鸭山"',u'句容':u'City="句容"',u'台州':u'City="台州"',u'合肥':u'City="合肥"',u'吉安':u'City="吉安"',u'吉林':u'City="吉林"',u'吐鲁番':u'City="吐鲁番"',u'吕梁':u'City="吕梁"',u'吴忠':u'City="吴忠"',u'吴江':u'City="吴江"',u'周口':u'City="周口"',u'呼伦贝尔':u'City="呼伦贝尔"',u'呼和浩特':u'City="呼和浩特"',u'和田':u'City="和田"',u'咸宁':u'City="咸宁"',u'咸阳':u'City="咸阳"',u'哈密':u'City="哈密"',u'哈尔滨':u'City="哈尔滨"',u'唐山':u'City="唐山"',u'商丘':u'City="商丘"',u'商洛':u'City="商洛"',u'喀什':u'City="喀什"',u'嘉兴':u'City="嘉兴"',u'嘉峪关':u'City="嘉峪关"',u'四平':u'City="四平"',u'固原':u'City="固原"',u'塔城':u'City="塔城"',u'大兴安岭':u'City="大兴安岭"',u'大同':u'City="大同"',u'大庆':u'City="大庆"',u'大理州':u'City="大理州"',u'大连':u'City="大连"',u'天水':u'City="天水"',u'天津':u'City="天津"',u'太仓':u'City="太仓"',u'太原':u'City="太原"',u'威海':u'City="威海"',u'娄底':u'City="娄底"',u'孝感':u'City="孝感"',u'宁德':u'City="宁德"',u'宁波':u'City="宁波"',u'安庆':u'City="安庆"',u'安康':u'City="安康"',u'安阳':u'City="安阳"',u'安顺':u'City="安顺"',u'定西':u'City="定西"',u'宜兴':u'City="宜兴"',u'宜宾':u'City="宜宾"',u'宜昌':u'City="宜昌"',u'宜春':u'City="宜春"',u'宝鸡':u'City="宝鸡"',u'宣城':u'City="宣城"',u'宿州':u'City="宿州"',u'宿迁':u'City="宿迁"',u'富阳':u'City="富阳"',u'寿光':u'City="寿光"',u'山南':u'City="山南"',u'岳阳':u'City="岳阳"',u'崇左':u'City="崇左"',u'巴中':u'City="巴中"',u'巴彦淖尔':u'City="巴彦淖尔"',u'常州':u'City="常州"',u'常德':u'City="常德"',u'常熟':u'City="常熟"',u'平凉':u'City="平凉"',u'平度':u'City="平度"',u'平顶山':u'City="平顶山"',u'广元':u'City="广元"',u'广安':u'City="广安"',u'广州':u'City="广州"',u'庆阳':u'City="庆阳"',u'库尔勒':u'City="库尔勒"',u'廊坊':u'City="廊坊"',u'延安':u'City="延安"',u'延边州':u'City="延边州"',u'开封':u'City="开封"',u'张家口':u'City="张家口"',u'张家港':u'City="张家港"',u'张家界':u'City="张家界"',u'张掖':u'City="张掖"',u'徐州':u'City="徐州"',u'德宏州':u'City="德宏州"',u'德州':u'City="德州"',u'德阳':u'City="德阳"',u'忻州':u'City="忻州"',u'怀化':u'City="怀化"',u'怒江州':u'City="怒江州"',u'恩施州':u'City="恩施州"',u'惠州':u'City="惠州"',u'成都':u'City="成都"',u'扬州':u'City="扬州"',u'承德':u'City="承德"',u'抚州':u'City="抚州"',u'抚顺':u'City="抚顺"',u'拉萨':u'City="拉萨"',u'招远':u'City="招远"',u'揭阳':u'City="揭阳"',u'攀枝花':u'City="攀枝花"',u'文山州':u'City="文山州"',u'文登':u'City="文登"',u'新乡':u'City="新乡"',u'新余':u'City="新余"',u'无锡':u'City="无锡"',u'日喀则':u'City="日喀则"',u'日照':u'City="日照"',u'昆山':u'City="昆山"',u'昆明':u'City="昆明"',u'昌吉州':u'City="昌吉州"',u'昌都':u'City="昌都"',u'昭通':u'City="昭通"',u'晋中':u'City="晋中"',u'晋城':u'City="晋城"',u'普洱':u'City="普洱"',u'景德镇':u'City="景德镇"',u'曲靖':u'City="曲靖"',u'朔州':u'City="朔州"',u'朝阳':u'City="朝阳"',u'本溪':u'City="本溪"',u'来宾':u'City="来宾"',u'杭州':u'City="杭州"',u'松原':u'City="松原"',u'林芝':u'City="林芝"',u'果洛州':u'City="果洛州"',u'枣庄':u'City="枣庄"',u'柳州':u'City="柳州"',u'株洲':u'City="株洲"',u'桂林':u'City="桂林"',u'梅州':u'City="梅州"',u'梧州':u'City="梧州"',u'楚雄州':u'City="楚雄州"',u'榆林':u'City="榆林"',u'武威':u'City="武威"',u'武汉':u'City="武汉"',u'毕节':u'City="毕节"',u'永州':u'City="永州"',u'汉中':u'City="汉中"',u'汕头':u'City="汕头"',u'汕尾':u'City="汕尾"',u'江门':u'City="江门"',u'江阴':u'City="江阴"',u'池州':u'City="池州"',u'沈阳':u'City="沈阳"',u'沧州':u'City="沧州"',u'河池':u'City="河池"',u'河源':u'City="河源"',u'泉州':u'City="泉州"',u'泰安':u'City="泰安"',u'泰州':u'City="泰州"',u'泸州':u'City="泸州"',u'洛阳':u'City="洛阳"',u'济南':u'City="济南"',u'济宁':u'City="济宁"',u'海东':u'City="海东"',u'海北州':u'City="海北州"',u'海南州':u'City="海南州"',u'海口':u'City="海口"',u'海西州':u'City="海西州"',u'海门':u'City="海门"',u'淄博':u'City="淄博"',u'淮北':u'City="淮北"',u'淮南':u'City="淮南"',u'淮安':u'City="淮安"',u'深圳':u'City="深圳"',u'清远':u'City="清远"',u'温州':u'City="温州"',u'渭南':u'City="渭南"',u'湖州':u'City="湖州"',u'湘潭':u'City="湘潭"',u'湘西州':u'City="湘西州"',u'湛江':u'City="湛江"',u'溧阳':u'City="溧阳"',u'滁州':u'City="滁州"',u'滨州':u'City="滨州"',u'漯河':u'City="漯河"',u'漳州':u'City="漳州"',u'潍坊':u'City="潍坊"',u'潮州':u'City="潮州"',u'濮阳':u'City="濮阳"',u'烟台':u'City="烟台"',u'焦作':u'City="焦作"',u'牡丹江':u'City="牡丹江"',u'玉林':u'City="玉林"',u'玉树州':u'City="玉树州"',u'玉溪':u'City="玉溪"',u'珠海':u'City="珠海"',u'瓦房店':u'City="瓦房店"',u'甘南州':u'City="甘南州"',u'甘孜州':u'City="甘孜州"',u'白城':u'City="白城"',u'白山':u'City="白山"',u'白银':u'City="白银"',u'百色':u'City="百色"',u'益阳':u'City="益阳"',u'盐城':u'City="盐城"',u'盘锦':u'City="盘锦"',u'眉山':u'City="眉山"',u'石嘴山':u'City="石嘴山"',u'石家庄':u'City="石家庄"',u'石河子':u'City="石河子"',u'福州':u'City="福州"',u'秦皇岛':u'City="秦皇岛"',u'章丘':u'City="章丘"',u'红河州':u'City="红河州"',u'绍兴':u'City="绍兴"',u'绥化':u'City="绥化"',u'绵阳':u'City="绵阳"',u'聊城':u'City="聊城"',u'肇庆':u'City="肇庆"',u'胶南':u'City="胶南"',u'胶州':u'City="胶州"',u'自贡':u'City="自贡"',u'舟山':u'City="舟山"',u'芜湖':u'City="芜湖"',u'苏州':u'City="苏州"',u'茂名':u'City="茂名"',u'荆州':u'City="荆州"',u'荆门':u'City="荆门"',u'荣成':u'City="荣成"',u'莆田':u'City="莆田"',u'莱州':u'City="莱州"',u'莱芜':u'City="莱芜"',u'莱西':u'City="莱西"',u'菏泽':u'City="菏泽"',u'萍乡':u'City="萍乡"',u'营口':u'City="营口"',u'葫芦岛':u'City="葫芦岛"',u'蓬莱':u'City="蓬莱"',u'蚌埠':u'City="蚌埠"',u'衡水':u'City="衡水"',u'衡阳':u'City="衡阳"',u'衢州':u'City="衢州"',u'襄阳':u'City="襄阳"',u'西双版纳州':u'City="西双版纳州"',u'西宁':u'City="西宁"',u'西安':u'City="西安"',u'许昌':u'City="许昌"',u'贵港':u'City="贵港"',u'贵阳':u'City="贵阳"',u'贺州':u'City="贺州"',u'资阳':u'City="资阳"',u'赣州':u'City="赣州"',u'赤峰':u'City="赤峰"',u'辽源':u'City="辽源"',u'辽阳':u'City="辽阳"',u'达州':u'City="达州"',u'运城':u'City="运城"',u'连云港':u'City="连云港"',u'迪庆州':u'City="迪庆州"',u'通化':u'City="通化"',u'通辽':u'City="通辽"',u'遂宁':u'City="遂宁"',u'遵义':u'City="遵义"',u'邢台':u'City="邢台"',u'那曲':u'City="那曲"',u'邯郸':u'City="邯郸"',u'邵阳':u'City="邵阳"',u'郑州':u'City="郑州"',u'郴州':u'City="郴州"',u'鄂尔多斯':u'City="鄂尔多斯"',u'鄂州':u'City="鄂州"',u'酒泉':u'City="酒泉"',u'重庆':u'City="重庆"',u'金华':u'City="金华"',u'金坛':u'City="金坛"',u'金昌':u'City="金昌"',u'钦州':u'City="钦州"',u'铁岭':u'City="铁岭"',u'铜仁':u'City="铜仁"',u'铜川':u'City="铜川"',u'铜陵':u'City="铜陵"',u'银川':u'City="银川"',u'锡林郭勒盟':u'City="锡林郭勒盟"',u'锦州':u'City="锦州"',u'镇江':u'City="镇江"',u'长春':u'City="长春"',u'长沙':u'City="长沙"',u'长治':u'City="长治"',u'阜新':u'City="阜新"',u'阜阳':u'City="阜阳"',u'防城港':u'City="防城港"',u'阳江':u'City="阳江"',u'阳泉':u'City="阳泉"',u'阿克苏':u'City="阿克苏"',u'阿勒泰':u'City="阿勒泰"',u'阿坝州':u'City="阿坝州"',u'阿拉善盟':u'City="阿拉善盟"',u'阿里':u'City="阿里"',u'陇南':u'City="陇南"',u'随州':u'City="随州"',u'雅安':u'City="雅安"',u'青岛':u'City="青岛"',u'鞍山':u'City="鞍山"',u'韶关':u'City="韶关"',u'马鞍山':u'City="马鞍山"',u'驻马店':u'City="驻马店"',u'鸡西':u'City="鸡西"',u'鹤壁':u'City="鹤壁"',u'鹤岗':u'City="鹤岗"',u'鹰潭':u'City="鹰潭"',u'黄冈':u'City="黄冈"',u'黄南州':u'City="黄南州"',u'黄山':u'City="黄山"',u'黄石':u'City="黄石"',u'黑河':u'City="黑河"',u'黔东南州':u'City="黔东南州"',u'黔南州':u'City="黔南州"',u'黔西南州':u'City="黔西南州"',u'齐齐哈尔':u'City="齐齐哈尔"',u'龙岩':u'City="龙岩"'}

    if wait2check in Citydict:
        return Citydict[wait2check]
    else:
        return 0



@asyncio.coroutine
def create_pool():
    global pool
    pool = yield from aiomysql.create_pool(host='localhost', port=3306,
                                           user='root', password='???',
                                           db='aircm', loop=loop,
                                           charset='utf8')
@asyncio.coroutine
def latest(request):

    query_parameter=request.rel_url.query
    if len(query_parameter)==1 and "city" in query_parameter and query_parameter.getone("city")!="":
        city_string = query_parameter.getone("city")
    else:
        return aiohttp.web.HTTPBadRequest()

    if city_string == "all":

        sql_latest = 'SELECT TimePoint,City,AQI,Trend FROM working WHERE TimePoint = (SELECT MAX(TimePoint) FROM working) ORDER BY AQI DESC;'

    else:
        city_list=city_string.split(",")

        if len(list(set(city_list)))!=len(city_list):#check duplication
            return aiohttp.web.HTTPBadRequest()

        sql_latest = 'SELECT TimePoint,City,AQI,Trend FROM (SELECT TimePoint,City,AQI,Trend FROM working WHERE TimePoint = (SELECT MAX(TimePoint) FROM working)) nearestHourTable WHERE'

        for city in city_list:
            add=valuecheck(city)
            if add == 0:
                return aiohttp.web.HTTPBadRequest()
            else:
                sql_latest = sql_latest + " " + add + " OR"

        sql_latest = sql_latest[:-3]+";"

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute(sql_latest)
        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()
    length=len(out)

    allData=[]
    for i in range(0,length):
        allData.append("placeholder")

    for i in range(0,length):

        oneCity = collections.OrderedDict()
        oneCity['update']=out[i][0].strftime('%Y-%m-%d %H:%M')
        oneCity['city']=out[i][1]
        oneCity['aqi']=out[i][2]
        oneCity['trend']=out[i][3]
        if city_string == "all":
            allData[i]=oneCity
        else:
            allData[city_list.index(out[i][1])]=oneCity

    return web.Response(text=json.dumps(allData,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

@asyncio.coroutine
def last4h(request):

    query_parameter=request.rel_url.query
    if len(query_parameter)==1 and "city" in query_parameter and query_parameter.getone("city")!="":
        city = query_parameter.getone("city")
    else:
        return aiohttp.web.HTTPBadRequest()

    sql_city_part=valuecheck(city)
    if sql_city_part == 0:
        return aiohttp.web.HTTPBadRequest()
    else:
        sql_last4h = "SELECT TimePoint,City,AQI FROM working WHERE " + sql_city_part + " AND TimePoint >= (SELECT DISTINCT TimePoint FROM working ORDER BY TimePoint DESC LIMIT 3,1) ORDER BY TimePoint;"

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute(sql_last4h)
        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()
    length=len(out)

    allData=[]

    for i in range(0,length):

        oneHour = collections.OrderedDict()
        oneHour['update']=out[i][0].strftime('%Y-%m-%d %H:%M')
        oneHour['city']=out[i][1]
        oneHour['aqi']=out[i][2]
        allData.append(oneHour)

    executetime=datetime.datetime.now()-starttime
    logger.info(str(executetime.seconds*1000+executetime.microseconds/1000)+"ms")

    return web.Response(text=json.dumps(allData,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')


@asyncio.coroutine
def now(request):
    starttime=datetime.datetime.now()
    city=request.match_info["city"]
    check=valuecheck(city)
    if check == 0:
        return aiohttp.web.HTTPBadRequest()

    sql_now = 'SELECT TimePoint,City,AQI,Trend,O3,CO,SO2,NO2,PM2_5,PM10 FROM (SELECT TimePoint,City,AQI,Trend,O3,CO,SO2,NO2,PM2_5,PM10 FROM working WHERE TimePoint = (SELECT MAX(TimePoint) FROM working)) nearestHourTable WHERE City="'+city+'";'

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute(sql_now)
        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()
    length=len(out)

    nowData = collections.OrderedDict()
    nowData['time']=out[0][0].strftime('%Y-%m-%d %H:%M')
    nowData['area']=out[0][1]
    nowData['aqi']=out[0][2]
    nowData['trend']=out[0][3]
    nowData['o3']=out[0][4]
    nowData['co']=float(out[0][5])if out[0][5]!=None else out[0][5]
    nowData['so2']=out[0][6]
    nowData['no2']=out[0][7]
    nowData['pm25']=out[0][8]
    nowData['pm10']=out[0][9]

    executetime=datetime.datetime.now()-starttime
    logger.info(starttime.strftime("%Y-%m-%m %H:%M:%S\t")+"ReturnLatestData\t"+city+"\t"+str(executetime.seconds*1000+executetime.microseconds/1000)+"ms")

    return web.Response(text=json.dumps(nowData,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

@asyncio.coroutine
def today(request):
    starttime=datetime.datetime.now()
    city=request.match_info["city"]
    check=valuecheck(city)
    if check == 0:
        return aiohttp.web.HTTPBadRequest()

    sql_today = 'SELECT TimePoint,City,AQI,Trend,O3,CO,SO2,NO2,PM2_5,PM10 FROM (SELECT TimePoint,City,AQI,Trend,O3,CO,SO2,NO2,PM2_5,PM10 FROM working WHERE TimePoint >= (SELECT DATE_FORMAT(MAX(TimePoint),"%Y-%m-%d 00:00") FROM working)) todayTable WHERE City="'+city+'";'

    #remove upper bound "AND TimePoint <=(SELECT MAX(TimePoint) FROM working)"

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute(sql_today)
        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()
    length=len(out)

    allData=[]

    for i in range(0,length):
        oneHour = collections.OrderedDict()
        oneHour['time']=out[i][0].strftime('%Y-%m-%d %H:%M')
        oneHour['area']=out[i][1]
        oneHour['aqi']=out[i][2]
        oneHour['trend']=out[i][3]
        oneHour['o3']=out[i][4]
        oneHour['co']=float(out[i][5])if out[i][5]!=None else out[i][5]
        oneHour['so2']=out[i][6]
        oneHour['no2']=out[i][7]
        oneHour['pm25']=out[i][8]
        oneHour['pm10']=out[i][9]
        allData.append(oneHour)

    executetime=datetime.datetime.now()-starttime
    logger.info(starttime.strftime("%Y-%m-%m %H:%M:%S\t")+"ReturnAllDayData\t"+city+"\t"+str(executetime.seconds*1000+executetime.microseconds/1000)+"ms")

    return web.Response(text=json.dumps(allData,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

@asyncio.coroutine
def cities(request):
    starttime=datetime.datetime.now()
    query_parameter=request.rel_url.query
    city_list=list(query_parameter.values())

    if len(list(set(city_list)))!=len(city_list) or len(city_list)==0:
        #duplication or empty
        return aiohttp.web.HTTPBadRequest()

    sql_cities = 'SELECT TimePoint,City,AQI,Trend,O3,CO,SO2,NO2,PM2_5,PM10 FROM (SELECT TimePoint,City,AQI,Trend,O3,CO,SO2,NO2,PM2_5,PM10 FROM working WHERE TimePoint = (SELECT MAX(TimePoint) FROM working)) nearestHourTable WHERE'

    for city in city_list:
        add=valuecheck(city)
        if add == 0:
            return aiohttp.web.HTTPBadRequest()
        else:
            sql_cities = sql_cities + " " + add + " OR"

    sql_cities = sql_cities[:-3]+";"

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute(sql_cities)
        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()
    length=len(out)

    allData=[]

    for i in range(0,length):
        allData.append("placeholder")

    for i in range(0,length):
        oneCity = collections.OrderedDict()
        oneCity['time']=out[i][0].strftime('%Y-%m-%d %H:%M')
        oneCity['area']=out[i][1]
        oneCity['aqi']=out[i][2]
        oneCity['trend']=out[i][3]
        oneCity['o3']=out[i][4]
        oneCity['co']=float(out[i][5])if out[i][5]!=None else out[i][5]
        oneCity['so2']=out[i][6]
        oneCity['no2']=out[i][7]
        oneCity['pm25']=out[i][8]
        oneCity['pm10']=out[i][9]
        allData[city_list.index(out[i][1])]=oneCity

    executetime=datetime.datetime.now()-starttime
    logger.info(starttime.strftime("%Y-%m-%m %H:%M:%S\t")+"ReturnFocusData \t"+str(city_list)+"\t"+str(executetime.seconds*1000+executetime.microseconds/1000)+"ms")

    return web.Response(text=json.dumps(allData,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')

@asyncio.coroutine
def allcity(request):
    starttime=datetime.datetime.now()
    allcity = 'SELECT DISTINCT City FROM working;'

    global pool
    with (yield from pool) as conn:
        cur = yield from conn.cursor()
        yield from cur.execute(allcity)
        out = yield from cur.fetchall()
        yield from cur.close()
        conn.close()
    length=len(out)

    allData=[]

    for i in range(0,length):
        oneCity={}
        oneCity['city']=out[i][0]
        allData.append(oneCity)

    executetime=datetime.datetime.now()-starttime
    logger.info(starttime.strftime("%Y-%m-%m %H:%M:%S\t")+"ReturnListOfCity\t"+str(executetime.seconds*1000+executetime.microseconds/1000)+"ms")

    return web.Response(text=json.dumps(allData,ensure_ascii=False,sort_keys=False),content_type='application/json',charset='utf-8')


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/getdata/last4h',last4h)
    app.router.add_route('GET', '/getdata/latest',latest)

    app.router.add_route('GET', '/aqi/{city}&now',now)
    app.router.add_route('GET', '/aqi/{city}&today',today)
    app.router.add_route('GET', '/aqi/cities',cities)
    app.router.add_route('GET', '/aqi/allcity',allcity)

    srv = yield from loop.create_server(app.make_handler(access_log=None), '127.0.0.1', 8081 )
    logger.info('Server started at port 8081...')
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(create_pool())
loop.run_until_complete(init(loop))
loop.run_forever()

