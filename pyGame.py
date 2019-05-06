#encoding: utf-8
import pygame
import time
import weatherAPI # It is coded by lee in weatherAPI.py
import SystemInfo	# It is coded by lee in SystemInfo.py

def ShowPicture(picturepath,x0,y0):  
    background=pygame.image.load(picturepath)
    background.convert_alpha()
    window.blit(background,(x0,y0))
    return
def ShowCircle():
    pygame.draw.circle(window,pygame.Color(255,255,255),(width/2,height/2),radius,fill)
    return
def ShowLine(x0,y0,x1,y1):
    pygame.draw.line(window,pygame.Color(255,255,255),(x0,y0),(x1,y1),fill)
    return
Yellow=(255,255,0)
Red=(255,0,0)
LightBlue=(190,190,255)
Green=(0,255,0)
Black=(0,0,0)
White=(255,255,255)
def ShowRec(x0,y0,x1,y1,color,fill):
    pygame.draw.rect(window,color,(x0,y0,x1,y1),fill)
    return

def ShowStr(mystring,x0,y0,size):
    font=pygame.font.Font('gkai00mp.ttf',size,bold=1)
    textSuface=font.render(mystring,1,pygame.Color(255,255,255))
    window.blit(textSuface,(x0,y0))                    
    return
#背景参数设置                            
width=1280
height=1024
fill=1
#初始化背景
pygame.init()
window=pygame.display.set_mode((width,height),pygame.FULLSCREEN)#全屏
#window=pygame.display.set_mode((width,height))#不全屏
window.fill(pygame.Color(255,255,255))

loop=0
last_ip = ip = ''
updatingtime=""
Title_X=width
WeatherValidation=False
while True:

    window.fill(pygame.Color(0,0,0))
   # ShowPicture("a_3.gif",20,450)
    #draw grids
    #ShowStr(u"时间",10,20,80)
    ShowRec(10,10,width-20,height-80,White,1)
    ShowLine(10,height/5,width-10,height/5)
    ShowLine(10,height/5*3,width-10,height/5*3)
    ShowLine(width/2,height/5,width/2,height-70)
    ShowLine(width/4,height/5*3,width/4,height-70)
    ShowLine(width/4*3,height/5*3,width/4*3,height-70)
    #time show                                                                   
    mylocaltime=time.localtime()
    myclock=time.strftime("%H:%M:%S",mylocaltime)#13:15:03 2017-04-21
    ShowStr(myclock,0,0,200)
    mydate=time.strftime("%Y-%m-%d",mylocaltime)#2017-04-21
    ShowStr(mydate,810,5,90)
    mytime=time.strftime("%A",mylocaltime)#Thursday
    ShowStr(mytime,810,100,90)
    #cpu_usage show
    ip = SystemInfo.get_ip('wlan0')
    cpu_usage =SystemInfo.getCPUuse()
    ShowStr(ip,width/2+20,height/5*2+160,48)
    ShowRec(width/2+20,height/5*2+110,cpu_usage/100*600+20,48,Yellow,0)
    ShowStr("CPU usage:"+str("%2d"%cpu_usage)+"%",width/2+20,height/5*2+110,48)
    
    #netspeed show
    NetInfoOld=SystemInfo.net_stat()
    time.sleep(1)
    NetInfoNew=SystemInfo.net_stat()
    DownloadSpeed=(NetInfoNew[0]["ReceiveBytes"]-NetInfoOld[0]["ReceiveBytes"])/1048576 #last second total flow -current second total flow 
    UploadSpeed=(NetInfoNew[0]["TransmitBytes"]-NetInfoOld[0]["TransmitBytes"])/1048576
    ShowRec(width/2+20,height/5*2+10,DownloadSpeed/10*600+20,48,Green,0)
    ShowRec(width/2+20,height/5*2+60,UploadSpeed/10*600+20,48,LightBlue,0)
    ShowStr("↓:"+str("%3.2f"%(DownloadSpeed))+"MB/s",width/2+20,height/5*2+10,48)
    ShowStr("↑:"+str("%3.2f"%(UploadSpeed))+"MB/s",width/2+20,height/5*2+60,48)

    
 #   print ("↓:"+str("%3.1f"%(DownloadSpeed))+"MB/s")
  #  print ("↑:"+str("%3.1f"%(UploadSpeed))+"MB/s")
    
    #print("CPU usage:"+str("%2d"%cpu_usage)+"%")
    
    #weather show
    if loop % 10800==0 : #update per 3 hours
        jsonArr=weatherAPI.GetWeatherInfo()
        if jsonArr!=None :#记录请求数据时间
            updatingtime=time.strftime("%H:%M:%S",mylocaltime)    
            if jsonArr["status"]!="0":
                print (jsonArr["msg"])
                WeatherValidation=False
            else:
                result=jsonArr["result"]
                WeatherValidation=True
                #print (result["city"],result["weather"],result["temp"],result["temphigh"],result["templow"])
    if WeatherValidation==True:
        AQI=result["aqi"]
        index=result["index"]
        index0=index[0]
        daily=result["daily"]
        day1=daily[1]#明天天气预报
        day2=daily[2]#明天天气预报
        day3=daily[3]#明天天气预报
        day4=daily[4]#明天天气预报              
    ##        #室外温湿度
        ShowPicture("pictures/"+result["img"]+".png",width/16,height/5+150)
        ShowStr(result["city"],20,height/5+10,100)
        ShowStr(result["weather"],width/32,height/5*2+50,120)
        ShowStr(result["temp"]+"℃",width/4,height/5,160)
        ShowStr("最高"+result["temphigh"]+"℃"+" "+"最低"+result["templow"]+"℃",width/4-90,height/5*2-20,48)
        ShowStr("湿度:"+result["humidity"]+"%",width/4,height/5*2+110,48)
        ShowStr(result["winddirect"],width/2+20,height/5+10,120)
        ShowStr(result["windpower"],width/2+50,height/5+140,64)
    ##        #空气质量
        ShowStr("PM2.5:",width/2+280,height/5+120,32)
        ShowStr(AQI["pm2_5"],width/2+400,height/5-20,200)
        ShowStr("空气质量:"+AQI["quality"],width/2+240,height/5*2-40,32)

        if Title_X<=-100:
            Title_X=width
        else:
            Title_X=Title_X-40
        ShowStr(index0["detail"],Title_X,height-50,40)
        #未来几天天气预报
        ShowStr(day1["date"],width/32,height/5*3+height/30,48)
        ShowStr(day1["day"]["weather"],width/32,height/5*3+height/5-40,100)
        ShowStr(day1["day"]["windpower"],width/32+70,height/5*3+height/10,64)
        ShowStr(day1["night"]["templow"]+"~"+day1["day"]["temphigh"]+"℃",width/32,height-130,64)
        ShowPicture("pictures/"+day1["day"]["img"]+".png",width/32,height/5*3+height/10)
    ##
        ShowStr(day2["date"],width/4+width/32,height/5*3+height/30,48)
        ShowStr(day2["day"]["weather"],width/4+width/32,height/5*3+height/5-40,100)
        ShowStr(day2["day"]["windpower"],width/4+width/32+70,height/5*3+height/10,64)
        ShowStr(day2["night"]["templow"]+"~"+day2["day"]["temphigh"]+"℃",width/4+width/32,height-130,64)
        ShowPicture("pictures/"+day2["day"]["img"]+".png",width/4+width/32,height/5*3+height/10)
    ##    
        ShowStr(day3["date"],width/4*2+width/32,height/5*3+height/30,48)
        ShowStr(day3["day"]["weather"],width/4*2+width/32,height/5*3+height/5-40,100)
        ShowStr(day3["day"]["windpower"],width/4*2+width/32+70,height/5*3+height/10,64)
        ShowStr(day3["night"]["templow"]+"~"+day2["day"]["temphigh"]+"℃",width/4*2+width/32,height-130,64)
        ShowPicture("pictures/"+day3["day"]["img"]+".png",width/4*2+width/32,height/5*3+height/10)
    ##    
        ShowStr(day4["date"],width/4*3+width/32,height/5*3+height/30,48)
        ShowStr(day4["day"]["weather"],width/4*3+width/32,height/5*3+height/5-40,100)
        ShowStr(day4["day"]["windpower"],width/4*3+width/32+70,height/5*3+height/10,64)
        ShowStr(day4["night"]["templow"]+"~"+day2["day"]["temphigh"]+"℃",width/4*3+width/32,height-130,64)
        ShowPicture("pictures/"+day4["day"]["img"]+".png",width/4*3+width/32,height/5*3+height/10)
    #记录请求数据时间
    ShowStr("Last update:"+updatingtime,width/4*3+20,height/5*3-30,24)
    
    #update 
    pygame.display.update()
    
    loop +=1
    #全屏
   #for event in pygame.event.get():
   #     if event.type==pygame.KEYDOWN:
   #         running=False
#pygame.quit()
