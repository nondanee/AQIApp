# AQIApp
The go project [chongg039/AQIApp](https://github.com/chongg039/AQIApp) rewrite by python

## About database
Please confirm that database charset is 'utf-8' because table raw contains chinese characters.  
SQL sentences for creating tables are provided in the file "init.sql" 

## About crawler

Coding with python 2.7+  
Crawler fetch authoritative data from the [official Silverlight application of Ministry of Environmental Protection of China](http://106.37.208.233:20035/)  

Based on the open-source object ["hebingchang/air-in-china"](https://github.com/hebingchang/air-in-china)  
Using an open-source third party library ["ernw/python-wcfbin"](https://github.com/ernw/python-wcfbin)  

Pay tribute to their developers!

Follow modules should be pip-installed if "ImportError"
```
pip install xmltodict		#import xmltodict
pip install future		#import builtins
pip install mysql-python	#import MySQLdb
pip install requests		#import requests
``` 

The raw data pulled down at the first step covers all stations from the whole country in that hour.  
Then SQL's AVG() function can help to calculate average values for a certain city.


## About server

Coding with python 3.4+  
Using web framework ["aiohttp"](http://aiohttp.readthedocs.io/en/stable/)
 
Follow modules should be pip-installed if "ImportError"
```
pip3 install aiohttp		#import aiohttp
pip3 install aiomysql		#import aiomysql
``` 

Interface definition in full accordance with the go-server written by [chongg039](https://github.com/chongg039).

Response data is formatted to JSON

### Below is some samples:

1. GetOneCityLatestData

GET `http://localhost:8088/aqi/成都&now`

*NOTICE: This response json don't have the outermost mark[]*

```json
{
	"time": "2017-03-14 21:00",
	"area": "成都",
	"aqi": 50,
	"trend": 1,
	"o3": 97,
	"co": 0.8,
	"so2": 12,
	"no2": 49,
	"pm25": 30,
	"pm10": 52
}
```

2. GetOneCityAllDayData

GET `http://localhost:8088/aqi/成都&today`

*NOTICE: Sort in time ascending order*

```json
[
	{
		"time": "2017-03-14 00:00",
		"area": "成都",
		"aqi": 42,
		"trend": 0,
		"o3": 93,
		"co": 1.0,
		"so2": 9,
		"no2": 75,
		"pm25": 16,
		"pm10": 34
	},
	{
		"time": "2017-03-14 01:00",
		"area": "成都",
		"aqi": 47,
		"trend": 1,
		"o3": 93,
		"co": 1.1,
		"so2": 10,
		"no2": 83,
		"pm25": 20,
		"pm10": 42
	},
	......
	{
		"time": "2017-03-14 21:00",
		"area": "成都",
		"aqi": 50,
		"trend": 1,
		"o3": 97,
		"co": 0.8,
		"so2": 12,
		"no2": 49,
		"pm25": 30,
		"pm10": 52
	}
]
```

3. GetSpecifyCitiesLatestData

GET `http://localhost:8088/aqi/cities?1=成都&2=北京&3=广州`
 
**NOTE: Nonsensitive with query-string's keys, allow duplicate keys but no duplicate values**

`http://localhost:8088/aqi/cities?city=成都&city=北京&city=广州` **[√]**  
`http://localhost:8088/aqi/cities?aaaa=成都&eeee=北京&bbbb=广州` **[√]**  
`http://localhost:8088/aqi/cities?aaaa=成都&eeee=北京&bbbb=北京` **[×]** 

```json
[
	{
		"time": "2017-03-14 21:00",
		"area": "成都",
		"aqi": 50,
		"trend": 1,
		"o3": 97,
		"co": 0.8,
		"so2": 12,
		"no2": 49,
		"pm25": 30,
		"pm10": 52
	},
	{
		"time": "2017-03-14 21:00",
		"area": "北京",
		"aqi": 93,
		"trend": 1,
		"o3": 95,
		"co": 0.8,
		"so2": 11,
		"no2": 64,
		"pm25": 41,
		"pm10": 136
	},
	{
		"time": "2017-03-14 21:00",
		"area": "广州",
		"aqi": 30,
		"trend": 0,
		"o3": 44,
		"co": 0.7,
		"so2": 9,
		"no2": 50,
		"pm25": 12,
		"pm10": 29
	}
]
```
4. (NEW)GetOneCityLast4hData

GET `http://localhost:8088/getdata/last4h?city=成都`

```json
[
	{
		"update": "2017-03-14 19:00",
		"city": "成都",
		"aqi": 44
	},
	{
		"update": "2017-03-14 20:00",
		"city": "成都",
		"aqi": 46
	},
	{
		"update": "2017-03-14 21:00",
		"city": "成都",
		"aqi": 50
	},
	{
		"update": "2017-03-14 22:00",
		"city": "成都",
		"aqi": 51
	}
]
```


5. (NEW)GetSpecifyCitiesLatestData

GET `http://localhost:8088/getdata/latest?city=成都,北京,广州`

```json
[
	{
		"update": "2017-03-14 21:00",
		"city": "成都",
		"aqi": 50,
		"trend": 1
	},
	{
		"update": "2017-03-14 21:00",
		"city": "北京",
		"aqi": 93,
		"trend": 1
	},
	{
		"update": "2017-03-14 21:00",
		"city": "广州",
		"aqi": 30,
		"trend": 0
	}
]
```

*TIPS: Citys' order in response data is sort by the order in request parameter*  

**ATTENTION: City's name no existing, Query Parameters' value duplication will trigger "400 : bad request" status code**

## About deployment

### For crawler
I use linux's "crontab" function to set a scheduled task running every 5 mins.  
Beacuse logging shows official website update their data close to half past an hour,  
I make the program check its start time before pulling data.  
*Can only run between 25 minutes and 35minutes past an hour*  
**If you know a better way, please notify me.**

### For server
I use supervisor (really unfriendly to chinese output, and can not guide python's print() to stdout)  
In order to log out sql-select costs, I use logging module and replace print() by logger.info()

Please add following parameters to the supervisor's program configuration file

```
loglevel=info			#set log out level
redirect_stderr=true		#logging is regard as stderr by default
stdout_logfile=...		#set directory for stdout file
```
P.S. I disable default aiohttp-access log
