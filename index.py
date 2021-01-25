# -*- coding:UTF-8 -*-

from flask import Flask, redirect, url_for, render_template
import json
import color
import time
from car_run import Car
from camera import Camera
from sensor import Sensor

app = Flask(__name__)

# index
@app.route('/')
def show_index():
    return render_template('index.html')

#rendering the HTML page which has the button
@app.route('/json1')
def json1():
    return render_template('index.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
    return ("nothing")

# for car test
@app.route('/car_run', methods=['GET', 'POST'])
def car_run():
    car = Car()
    car.forward()
    color.show()
    car.stop()
    return render_template('index.html')

# 小车
@app.route('/car_fwd')
def car_fwd():
    car = Car()
    car.forward()
    return ("nothing")

@app.route('/car_bwd')
def car_bwd():
    car = Car()
    car.backward()
    return ("nothing")

@app.route('/car_left')
def car_left():
    car = Car()
    car.leftturn()
    return ("nothing")

@app.route('/car_right')
def car_right():
    car = Car()
    car.rightturn()
    return ("nothing")

@app.route('/car_stop')
def car_stop():
    car = Car()
    car.stop()
    return ("nothing")

# 超声波雷达避障自主行走
@app.route('/radar_self_drive/<isEnable>', methods=['GET', 'POST'])
def radar_self_drive(isEnable):
    print 'radar_self_drive ' + str(isEnable)
    car = Car()
    car.buzzer(True)
    time.sleep(0.2)
    car.buzzer(False)
    if('true'==isEnable) :
    	car.radar_self_drive(True)
    else :
	car.radar_self_drive(False)

# 摄像头
@app.route('/camera_up')
def camera_up():
    cam = Camera()
    cam.up()
    return ("nothing")

@app.route('/camera_down')
def camera_down():
    cam = Camera()
    cam.down()
    return ("nothing")

@app.route('/camera_left')
def camera_left():
    cam = Camera()
    cam.left()
    return ("nothing")

@app.route('/camera_right')
def camera_right():
    cam = Camera()
    cam.right()
    return ("nothing")

@app.route('/camera_stop')
def camera_stop():
    cam = Camera()
    cam.stop()
    return ("nothing")

@app.route('/camera_reset')
def camera_reset():
    cam = Camera()
    cam.reset()
    return ("nothing")

# 七彩灯
@app.route('/light_on', methods=['GET', 'POST'])
def light_on():
    color.on()
    return ("nothing")

@app.route('/light_off', methods=['GET', 'POST'])
def light_off():
    color.off()
    return ("nothing")

# 蜂鸣器
@app.route('/buzzer/<buzzeron>', methods=['GET', 'POST'])
def buzzer(buzzeron):
    car = Car()
    print "car buzzeron="+str(buzzeron)
    if buzzeron == 'true':
        car.buzzer(True)
    else:
        car.buzzer(False)
    return ("nothing")

# 雷达舵机
@app.route('/radar_left')
def radar_left():
    cam = Camera()
    cam.radar_left()
    return ("nothing")

@app.route('/radar_right')
def radar_right():
    cam = Camera()
    cam.radar_right()
    return ("nothing")

@app.route('/radar_stop')
def radar_stop():
    cam = Camera()
    cam.radar_stop()
    return ("nothing")

@app.route('/radar_reset')
def radar_reset():
    cam = Camera()
    cam.radar_reset()
    return ("nothing")

@app.route('/radar_reset_left')
def radar_reset_left():
    cam = Camera()
    cam.radar_reset_left() 
    return ("nothing")

@app.route('/radar_reset_right')
def radar_reset_right():
    cam = Camera()
    cam.radar_reset_right() 
    return ("nothing")

#传感器
#红外
@app.route('/infrared_sensor', methods=['GET', 'POST'])
def infrared_sensor():
    sen = Sensor()
    print "红外:"
    print sen.infrared_sensor()
    ret = {}
    ret['infrared_sensor'] = sen.infrared_sensor()
    json_str = json.dumps(ret)
    return json_str

#所有传感器
@app.route('/sensor', methods=['GET', 'POST'])
def sensor():
    sen = Sensor()
    '''
    print "红外:"
    print sen.infrared_sensor()
    print "循迹:"
    print sen.track_sensor()
    print "光敏电阻:"
    print sen.light_sensor()
    print "超声波雷达测距(单位cm):"
    print sen.radar_distance_calculate()
    '''
    ret = {}
    ret['infrared_sensor'] = sen.infrared_sensor()
    ret['track_sensor'] = sen.track_sensor()
    ret['light_sensor'] = sen.light_sensor()
    ret['radar_distance_calculate'] = sen.radar_distance_calculate()
    json_str = json.dumps(ret)
    return json_str






if __name__ == '__main__':
    app.run("0.0.0.0",3000)
