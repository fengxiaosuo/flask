#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import threading
import sys
import color
from sensor import Sensor
from camera import Camera

#小车电机引脚定义
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#蜂鸣器引脚定义
buzzer = 8

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

g_radar_self_drive = False

class Car:
  _instance_lock = threading.Lock()
  pwm_ENA = None
  pwm_ENB = None

  # 一个类只允许一个实例
  def __new__(cls, *args, **kwargs):
    if not hasattr(Car, "_instance"):
        with Car._instance_lock:
            if not hasattr(Car, "_instance"):
                # 类加括号就回去执行__new__方法，__new__方法会创建一个类实例：Car()
                Car._instance = object.__new__(cls)  # 继承object类的__new__方法，类去调用方法，说明是函数，要手动传cls
    print 'new Car ret='+str(Car._instance)
    return Car._instance  #obj1
  
  def __init__(self):
    #电机引脚初始化操作
    GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
    GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
    GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
    #设置pwm引脚和频率为2000hz
    if Car.pwm_ENA == None :
        Car.pwm_ENA = GPIO.PWM(ENA, 2000)
    if Car.pwm_ENB == None :
        Car.pwm_ENB = GPIO.PWM(ENB, 2000)
    #蜂鸣器
    GPIO.setup(buzzer,GPIO.OUT,initial=GPIO.HIGH)

  #小车前进
  def forward(self, speed=100, speed2=100):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    #启动PWM设置占空比为100（0--100）
    Car.pwm_ENA.start(speed)
    Car.pwm_ENB.start(speed2)

  #小车后退
  def backward(self, speed=100, speed2=100):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    #启动PWM设置占空比为100（0--100）
    Car.pwm_ENA.start(speed)
    Car.pwm_ENB.start(speed2)

  #小车左转
  def leftturn(self, speed=100, speed2=100):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    #启动PWM设置占空比为100（0--100）
    Car.pwm_ENA.start(speed)
    Car.pwm_ENB.start(speed2)

  #小车右转
  def rightturn(self, speed=100, speed2=100):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    #启动PWM设置占空比为100（0--100）
    Car.pwm_ENA.start(speed)
    Car.pwm_ENB.start(speed2)

  #小车掉头
  def uturn(self):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    #启动PWM设置占空比为100（0--100）
    Car.pwm_ENA.start(100)
    Car.pwm_ENB.start(100)

  #小车原地左转
  def spin_left(self, speed=80, speed2=80):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    Car.pwm_ENA.ChangeDutyCycle(speed)
    Car.pwm_ENB.ChangeDutyCycle(speed2)

  #小车原地右转
  def spin_right(self, speed=80, speed2=80):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    Car.pwm_ENA.ChangeDutyCycle(speed)
    Car.pwm_ENB.ChangeDutyCycle(speed2)

  #小车停止
  def stop(self):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    #启动PWM设置占空比为100（0--100）
    Car.pwm_ENA.stop()
    Car.pwm_ENB.stop()

  #小车鸣笛
  def buzzer(self, buzzeron):
    print(sys._getframe().f_code.co_name)
    if buzzeron :
        GPIO.output(buzzer, GPIO.LOW)
    else :
        GPIO.output(buzzer, GPIO.HIGH)

  #舵机旋转超声波测距避障，led根据车的状态显示相应的颜色
  def avoid_collision(self):
    print("!!! "+sys._getframe().f_code.co_name)
    #开红灯
    color.red()
    #获取雷达instance
    sen = Sensor()
    #获取camera instance
    cam = Camera()
    #先退一点点
    self.backward(50, 50)
    time.sleep(0.5)
    self.stop()
	
    #舵机旋转到0度，即右侧，测距
    cam.radar_reset_right()
    time.sleep(0.5)
    rightdistance = sen.radar_distance_calculate()
    print 'rightdistance='+str(rightdistance)
    #舵机旋转到180度，即左侧，测距
    cam.radar_reset_left()
    time.sleep(0.5)
    leftdistance = sen.radar_distance_calculate()
    print 'leftdistance='+str(leftdistance)
    #舵机旋转到90度，即前方，测距
    cam.radar_reset()
    time.sleep(0.5)
    frontdistance = sen.radar_distance_calculate()
    print 'frontdistance='+str(frontdistance)
    
    if leftdistance < 30 and rightdistance < 30 and frontdistance < 30:
        #亮白色，掉头
        color.on()
        self.spin_right(85, 85)
        time.sleep(1)
    elif leftdistance >= rightdistance:
        #亮蓝色
        color.blue()
        self.spin_left(85, 85)
        time.sleep(0.5)
    elif leftdistance <= rightdistance:
        #亮绿色，向右转
        color.green()
        self.spin_right(85, 85)
        time.sleep(0.5)

    print("!!! quit !!! "+sys._getframe().f_code.co_name)
    return

  # 超声波雷达避障自主行走
  def radar_self_drive(self, isEnable):
    print(sys._getframe().f_code.co_name)
    global g_radar_self_drive
    print 'radar_self_drive isEnable=' + str(isEnable)
    print 'radar_self_drive g_radar_self_drive=' + str(g_radar_self_drive)
    g_radar_self_drive = isEnable
    sen = Sensor()
    while g_radar_self_drive:
        distance = sen.radar_distance_calculate()
        print "dis="+str(distance)
        if distance > 50:
            #先检查红外避障
            #遇到障碍物,红外避障模块的指示灯亮,端口电平为LOW
            #未遇到障碍物,红外避障模块的指示灯灭,端口电平为HIGH
            ret = sen.infrared_sensor()
            LeftSensorValue = ret[0]
            RightSensorValue = ret[1]
            print "LeftSensorValue="+str(LeftSensorValue) + " RightSensorValue="+str(RightSensorValue)
            if LeftSensorValue == True and RightSensorValue == True :
                self.forward()         #当两侧均未检测到障碍物时调用前进函数
            elif LeftSensorValue == True and RightSensorValue == False :
                self.spin_left(85, 85)     #右边探测到有障碍物，有信号返回，原地向左转
                time.sleep(0.5)
            elif RightSensorValue == True and LeftSensorValue == False:
                self.spin_right(85, 85)    #左边探测到有障碍物，有信号返回，原地向右转
                time.sleep(0.5)				
            elif RightSensorValue == False and LeftSensorValue == False :
                self.spin_right(85, 85)    #当两侧均检测到障碍物时调用固定方向的避障(原地右转)
                time.sleep(0.5)
            self.forward(50, 50)
        elif 30 <= distance <= 50:
            #先检查红外避障
            #遇到障碍物,红外避障模块的指示灯亮,端口电平为LOW
            #未遇到障碍物,红外避障模块的指示灯灭,端口电平为HIGH
            ret = sen.infrared_sensor()
            LeftSensorValue = ret[0]
            RightSensorValue = ret[1]
            print "LeftSensorValue="+str(LeftSensorValue) + " RightSensorValue="+str(RightSensorValue)
            if LeftSensorValue == True and RightSensorValue == True :
                self.forward()         #当两侧均未检测到障碍物时调用前进函数
            elif LeftSensorValue == True and RightSensorValue == False :
                self.spin_left(85, 85)     #右边探测到有障碍物，有信号返回，原地向左转
                time.sleep(0.5)
            elif RightSensorValue == True and LeftSensorValue == False:
                self.spin_right(85, 85)    #左边探测到有障碍物，有信号返回，原地向右转
                time.sleep(0.5)				
            elif RightSensorValue == False and LeftSensorValue == False :
                self.spin_right(85, 85)    #当两侧均检测到障碍物时调用固定方向的避障(原地右转)
                time.sleep(0.5)
            self.forward(50, 50)
        elif distance < 30:
            self.avoid_collision()


'''

car = Car()
car.radar_self_drive(True)
'''
'''
time.sleep(10)
car.stop()
'''
