## 环境依赖
- paho-mqtt==1.5.0


## 目录介绍
```
 ├── EMQ                            //项目文件夹
 |    |--client                    　//核心代码
 |    |--utils                      　//工具类
 │
 ├── EMQ_demo                      //示例demo
 │
 ├── README.md                     //README
 │
 ├── requirements.txt              //依赖库
 │ 
 └── shadow.json                   //应用影子配置文件
```


## 定时任务

### type类型
    interval:
        参数	                            说明
        weeks (int)	                    间隔几周
        days (int)	                    间隔几天
        hours (int)	                    间隔几小时
        minutes (int)	                间隔几分钟
        seconds (int)	                间隔多少秒


    date
        参数	                            说明
        run_date (datetime 或 str)	    作业的运行日期或时间
        
    cron
        参数	                            说明
        year (int 或 str)	            年，4位数字
        month (int 或 str)	            月 (范围1-12)
        day (int 或 str)	            日 (范围1-31
        week (int 或 str)	            周 (范围1-53)
        day_of_week (int 或 str)	    周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun)
        hour (int 或 str)	            时 (范围0-23)
        minute (int 或 str)	            分 (范围0-59)
        second (int 或 str)	            秒 (范围0-59)
