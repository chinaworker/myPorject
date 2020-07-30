import requests
import json
import time


desp, status = '', ''
sckey = 'SCU62271Te68100a706158bd4416cf502f331360b5d8998e48cdaa'
city = '邵阳县'
appkey = '8ff1f6e2dc2331ff96289fcd9c8a14d4'


def getweather():
    global desp, city, status
    url = ('https://way.jd.com/jisuapi/weather?city={}&cityid=&citycode=&appkey={}'.format(city, appkey))
    weather_res = requests.get(url=url).text
    weather_res = json.loads(weather_res)
    status = weather_res['code']
    result = weather_res['result']['result']
    date = result['date']
    week = result['week']
    city = result['city']
    weather = result['weather']
    hum = result['humidity']
    pm25 = result['aqi']['pm2_5']
    pm10 = result['aqi']['pm10']
    quality = result['aqi']['quality']
    winddirect = result['winddirect']
    windpower = result['windpower']
    affect = result['aqi']['aqiinfo']['affect']
    measure = result['aqi']['aqiinfo']['measure']
    today_temp = result['temp']
    today_temphigh = result['temphigh']
    today_templow = result['templow']
    ivalue = result['index'][6]['ivalue']
    detail = result['index'][6]['detail']
    hourly_weather = result['hourly'][0]['weather']
    hourly_temp = result['hourly'][0]['temp']
    hourly_time = result['hourly'][0]['time']
    loc_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    desp = (
        '##'+'-'*10+city+'-'*10+'\n'
        '#####'+'-'*10+loc_time+'-'*10+week+'\n'
        '####空气质量：'+str(quality)+'\n'
        '#####'+'pm2.5：'+str(pm25)+'\n'
        '#####'+'pm10：'+str(pm10)+'\n'
        '#####'+'空气影响：'+str(affect)+'\n'
        '#####'+'适合正常活动：'+str(measure)+'\n'
        '#### 天气状况：\n'
        '#####最低温度'+str(today_templow)+'℃'+'~'+'最高温度' +
        str(today_temphigh)+'℃'+'\n'
        '#####气温:'+str(today_temp)+'℃'+'\n'
        '#####天气：'+str(weather)+'\n'
        '#####'+str(ivalue)+'\n'
        '#####'+str(detail)+'\n'
        '#####'+str(winddirect)+str(windpower)+'\n'
        '#####下个小时的天气：'+hourly_weather+'\n'
        '#####气温：'+hourly_temp+'℃')


def upserver():
    global desp, sckey
    data = {
        'text': '天气预报',
        'desp': desp
    }
    url = ('https://sc.ftqq.com/%s.send' % sckey)
    server = requests.post(url=url, data=data)


def main():
    global status, city, sckey
    getweather()
    if status != '10000':
        print(status)
        status = '获取失败'
        print(status)
        url = ('https://sc.ftqq.com/%s.send' % sckey)
        data = {
            'text': '天气预报推送失败',
            'desp': '天气预报推送失败'
        }
        server = requests.post(url=url, data=data)
    else:
        upserver()


if __name__ == "__main__":
    main()
