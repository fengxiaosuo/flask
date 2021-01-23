#-*- coding:UTF-8 -*-
#本次舵机转动控制七彩灯控制舵机采用的是系统的pwm库
import RPi.GPIO as GPIO
import time
import threading


#RGB三色灯引脚定义
LED_R = 22
LED_G = 27
LED_B = 24

#舵机引脚定义
FrontServoPin = 23
ServoUpDownPin = 9
ServoLeftRightPin = 11

#设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BCM)

#忽略警告信息
GPIO.setwarnings(False)

#初始化上下左右角度为90度
g_leftright_pos = 90
g_updown_pos = 90

class Camera(object):
  _instance_lock = threading.Lock()
  allow_leftright_moving = 0
  allow_updown_moving = 0
  updown_servo = None
  leftright_servo = None

  # 一个类只允许一个实例
  def __new__(cls, *args, **kwargs):
    if not hasattr(Camera, "_instance"):
        with Camera._instance_lock:
            if not hasattr(Camera, "_instance"):
                # 类加括号就回去执行__new__方法，__new__方法会创建一个类实例：Camera()
                Camera._instance = object.__new__(cls)  # 继承object类的__new__方法，类去调用方法，说明是函数，要手动传cls
    print 'new camera ret='+str(Camera._instance)
    return Camera._instance  #obj1

  def __init__(self):
    #舵机引脚设置为输出模式
    GPIO.setup(ServoUpDownPin, GPIO.OUT)
    GPIO.setup(ServoLeftRightPin, GPIO.OUT)
    #设置pwm引脚和频率为50hz
    if Camera.updown_servo == None :
        Camera.updown_servo = GPIO.PWM(ServoUpDownPin, 50)
    if Camera.leftright_servo == None :
        Camera.leftright_servo = GPIO.PWM(ServoLeftRightPin, 50)
    Camera.updown_servo.start(0)
    Camera.leftright_servo.start(0)
    
  #摄像头舵机左右旋转到指定角度
  def leftrightservo_appointed_detection(self, pos): 
    for i in range(1):
    	Camera.leftright_servo.ChangeDutyCycle(2.5 + 10 * pos/180)
    	time.sleep(0.02)							#等待20ms周期结束
    	#Camera.leftright_servo.ChangeDutyCycle(0)	#归零信号

  #摄像头舵机上下旋转到指定角度
  def updownservo_appointed_detection(self, pos):  
    for i in range(1):  
    	Camera.updown_servo.ChangeDutyCycle(2.5 + 10 * pos/180)
    	time.sleep(0.02)							#等待20ms周期结束
    	#Camera.updown_servo.ChangeDutyCycle(0)	    #归零信号

  def up(self):
    print 'up'
    Camera.allow_updown_moving = 1
    global g_updown_pos
    pos = g_updown_pos
    print 'down pos='+str(pos)
    while Camera.allow_updown_moving == 1:
        print ('down='+str(pos) + ' Camera.allow_updown_moving='+str(Camera.allow_updown_moving))
        self.updownservo_appointed_detection(pos)
        pos += 0.7
        g_updown_pos = pos
        if g_updown_pos >= 180:
            g_updown_pos = 180
            break

  def down(self):
    print 'up'
    Camera.allow_updown_moving = 1
    global g_updown_pos
    pos = g_updown_pos
    print 'down pos='+str(pos)
    while Camera.allow_updown_moving == 1:
        print ('down='+str(pos) + ' Camera.allow_updown_moving='+str(Camera.allow_updown_moving))
        self.updownservo_appointed_detection(pos)
        pos -= 0.7
        g_updown_pos = pos
        if g_updown_pos <= 45:
            g_updown_pos = 45
            break

  def left(self):
    print 'left'
    Camera.allow_leftright_moving = 1
    global g_leftright_pos
    pos = g_leftright_pos
    print 'left pos='+str(pos)
    while Camera.allow_leftright_moving == 1:
        print ('left='+str(pos) + ' Camera.allow_leftright_moving='+str(Camera.allow_leftright_moving))
        self.leftrightservo_appointed_detection(pos)
        pos += 0.7
        g_leftright_pos = pos
        if g_leftright_pos >= 180:
            g_leftright_pos = 180
            break

  def right(self):
    print 'right'
    Camera.allow_leftright_moving = 1
    global g_leftright_pos
    pos = g_leftright_pos
    while Camera.allow_leftright_moving == 1:
        print ('left='+str(pos) + ' Camera.allow_leftright_moving='+str(Camera.allow_leftright_moving))
        self.leftrightservo_appointed_detection(pos)
        pos -= 0.7
        g_leftright_pos = pos
        if g_leftright_pos <= 0:
            g_leftright_pos =  0
            break

  def stop(self):
    Camera.allow_leftright_moving = 0
    Camera.allow_updown_moving = 0

  def reset(self):
    self.leftrightservo_appointed_detection(90)
    self.updownservo_appointed_detection(90)
    time.sleep(1)
