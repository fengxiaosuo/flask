#-*- coding:UTF-8 -*-
#获取四驱小车的各种传感器值
import RPi.GPIO as GPIO
import time
import threading
import sys

#小车按键定义
KeyPin = 8

#红外避障引脚定义
AvoidSensorLeft = 12
AvoidSensorRight = 17

#循迹红外引脚定义
#TrackSensorLeftPin1 TrackSensorLeftPin2 TrackSensorRightPin1 TrackSensorRightPin2
#      3                 5                  4                   18
TrackSensorLeftPin1  =  3   #定义左边第一个循迹红外传感器引脚为3口
TrackSensorLeftPin2  =  5   #定义左边第二个循迹红外传感器引脚为5口
TrackSensorRightPin1 =  4   #定义右边第一个循迹红外传感器引脚为4口
TrackSensorRightPin2 =  18  #定义右边第二个循迹红外传感器引脚为18口

#光敏电阻引脚定义
LdrSensorLeft = 7
LdrSensorRight = 6

#超声波雷达引脚定义，一个发射一个接收
EchoPin = 0
TrigPin = 1

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

class Sensor(object):
  _instance_lock = threading.Lock()
  allow_leftright_moving = 0
  allow_updown_moving = 0
  allow_radar_moving = 0
  updown_servo = None
  leftright_servo = None
  radar_servo = None

  # 一个类只允许一个实例
  def __new__(cls, *args, **kwargs):
    if not hasattr(Sensor, "_instance"):
        with Sensor._instance_lock:
            if not hasattr(Sensor, "_instance"):
                # 类加括号就回去执行__new__方法，__new__方法会创建一个类实例：Sensor()
                Sensor._instance = object.__new__(cls)  # 继承object类的__new__方法，类去调用方法，说明是函数，要手动传cls
    print 'new Sensor ret='+str(Sensor._instance)
    return Sensor._instance  #obj1

  def __init__(self):
    #按键引脚初始化为输入模式
    GPIO.setup(KeyPin,GPIO.IN)
    #红外避障引脚初始化为输入模式
    GPIO.setup(AvoidSensorLeft,GPIO.IN)
    GPIO.setup(AvoidSensorRight,GPIO.IN)
    #寻迹引脚初始化为输入模式
    GPIO.setup(TrackSensorLeftPin1,GPIO.IN)
    GPIO.setup(TrackSensorLeftPin2,GPIO.IN)
    GPIO.setup(TrackSensorRightPin1,GPIO.IN)
    GPIO.setup(TrackSensorRightPin2,GPIO.IN)
    #光敏电阻引脚初始化为输入模式
    GPIO.setup(LdrSensorLeft,GPIO.IN)
    GPIO.setup(LdrSensorRight,GPIO.IN)
    #超声波引脚初始化
    GPIO.setup(EchoPin,GPIO.IN)
    GPIO.setup(TrigPin,GPIO.OUT)
    
  #红外左，右
  def infrared_sensor(self) :
    left  = GPIO.input(AvoidSensorLeft)
    right  = GPIO.input(AvoidSensorRight)
    return left, right

  #循迹1,2,3,4传感器
  def track_sensor(self) :
    #检测到黑线时循迹模块相应的指示灯亮，端口电平为LOW
    #未检测到黑线时循迹模块相应的指示灯灭，端口电平为HIGH
    TrackSensorLeftValue1  = GPIO.input(TrackSensorLeftPin1)
    TrackSensorLeftValue2  = GPIO.input(TrackSensorLeftPin2)
    TrackSensorRightValue1 = GPIO.input(TrackSensorRightPin1)
    TrackSensorRightValue2 = GPIO.input(TrackSensorRightPin2)
    return TrackSensorLeftValue1, TrackSensorLeftValue2, TrackSensorRightValue1, TrackSensorRightValue2
    
  #光敏电阻左，右
  def light_sensor(self) :
    left  = GPIO.input(LdrSensorLeft)
    right  = GPIO.input(LdrSensorRight)
    return left, right
    
  #超声波函数
  def radar_distance_calculate(self):
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)
    while not GPIO.input(EchoPin):
        pass
    t1 = time.time()
    while GPIO.input(EchoPin):
        pass
    t2 = time.time()
    time.sleep(0.01)
    distance = ((t2 - t1)* 340 / 2) * 100
    print(sys._getframe().f_code.co_name + "distance is %d " % (((t2 - t1)* 340 / 2) * 100)) + "cm"
    return distance

'''
sen = Sensor()
while True:
    print "红外:"
    print sen.infrared_sensor()
    print "循迹:"
    print sen.track_sensor()
    print "光敏电阻:"
    print sen.light_sensor()
    print "超声波雷达测距(单位cm):"
    print sen.radar_distance_calculate()
    time.sleep(1)
'''