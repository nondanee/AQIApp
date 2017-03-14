## AQI app

https://github.com/hebingchang/air-in-china


## About database

Please confirm that database charset is 'utf-8' because table raw contains chinese characters 

Sql sentences for creating tables are provided in file "init.sql" 

## About crawler
Crawler fetch official data from the [official Silverlight application of Ministry of Environmental Protection of China](http://106.37.208.233:20035/)

Based on open-source object ["hebingchang/air-in-china"](https://github.com/hebingchang/air-in-china) 
Using open-source library ["python-wcfbin"](https://github.com/ernw/python-wcfbin) 

Coding with python 2.7+

Follow modules should be pip-installed if "ImportError"
```
pip install xmltodict #import xmltodict
pip install future #import builtins
pip install mysql-python #import MySQLdb
``` 

Beacuse logging shows official website update their data close to half past an hour 

I use linux's "crontab" function to set scheduled tasks running every 5 mins, 

and check the start time before pulling data.

If you find a better way, please notify me.

The data pulled down is the all stations' data in the whole country.

Once updated data got, sql's AVG() function can help to calculate average value for certain city 


## About server

Coding with python 3.4+

Using framework "aiohttp"

Follow modules should be pip-installed if "ImportError"
```
pip3 install aiohttp
pip3 install aiomysql
``` 

Url rounters compliy with the server written by go.

Response data is formatted to JSON

Below is some samples:

1.OneCityLatestData

GET `http://localhost:8088/aqi/成都&now`

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

2.OneCityAllDayData

GET `http://localhost:8088/aqi/成都&today`：返回当天所有的`JSON`数据

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

3.SpecifyCitiesLatestData


GET `http://localhost:8088/aqi/成都&2017021001`

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

P.S. Cityname no exists, Query list duplication will trigger "400 bad request"


## use supervisor for server deployment

Please add following parameters to configuration file

```
loglevel=info
redirect_stderr=true
stdout_logfile=...
```
P.S. I disable default aiohttp-access log
