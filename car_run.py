#-*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

#小车电机引脚定义
IN1 = 20
IN2 = 21
IN3 = 19
IN4 = 26
ENA = 16
ENB = 13

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

class Car:
  def __init__(self):
    pass

  #电机引脚初始化操作
  def motor_init(self):
    # run only once
    try:
        self.value
    except AttributeError:
        self.value = 0
        print('first time motor init')

        global pwm_ENA
        global pwm_ENB
        GPIO.setup(ENA,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(ENB,GPIO.OUT,initial=GPIO.HIGH)
        GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
        GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)
        #设置pwm引脚和频率为2000hz
        pwm_ENA = GPIO.PWM(ENA, 2000)
        pwm_ENB = GPIO.PWM(ENB, 2000)

  #小车前进
  def forward(self):
    self.motor_init()
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    #启动PWM设置占空比为100（0--100）
    pwm_ENA.start(100)
    pwm_ENB.start(100)

  #小车后退
  def backward(self):
    self.motor_init()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    #启动PWM设置占空比为100（0--100）
    pwm_ENA.start(100)
    pwm_ENB.start(100)

  #小车左转
  def leftturn(self):
    self.motor_init()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    #启动PWM设置占空比为100（0--100）
    pwm_ENA.start(100)
    pwm_ENB.start(100)

  #小车右转
  def rightturn(self):
    self.motor_init()
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    #启动PWM设置占空比为100（0--100）
    pwm_ENA.start(100)
    pwm_ENB.start(100)

  #小车掉头
  def uturn(self):
    self.motor_init()
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    #启动PWM设置占空比为100（0--100）
    pwm_ENA.start(100)
    pwm_ENB.start(100)

  #小车停止
  def stop(self):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    #启动PWM设置占空比为100（0--100）
    pwm_ENA.stop()
    pwm_ENB.stop()

#car = Car()
#car.forward()
#time.sleep(1)
#car.stop()









