#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time
import threading
import sys

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
  def forward(self):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    #启动PWM设置占空比为100（0--100）
    Car.pwm_ENA.start(100)
    Car.pwm_ENB.start(100)

  #小车后退
  def backward(self):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    #启动PWM设置占空比为100（0--100）
    Car.pwm_ENA.start(100)
    Car.pwm_ENB.start(100)

  #小车左转
  def leftturn(self):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    #启动PWM设置占空比为100（0--100）
    Car.pwm_ENA.start(100)
    Car.pwm_ENB.start(100)

  #小车右转
  def rightturn(self):
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    #启动PWM设置占空比为100（0--100）
    Car.pwm_ENA.start(100)
    Car.pwm_ENB.start(100)

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
  def spin_left():
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    Car.pwm_ENA.ChangeDutyCycle(80)
    Car.pwm_ENB.ChangeDutyCycle(80)

  #小车原地右转
  def spin_right():
    print(sys._getframe().f_code.co_name)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    Car.pwm_ENA.ChangeDutyCycle(80)
    Car.pwm_ENB.ChangeDutyCycle(80)

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




#car = Car()
#car.forward()
#time.sleep(1)
#car.stop()









