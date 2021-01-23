# -*- coding:UTF-8 -*-

from flask import Flask, redirect, url_for, render_template
import color
from car_run import Car
from camera import Camera

app = Flask(__name__)

@app.route('/')
def show_index():
    return render_template('index.html')

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

#rendering the HTML page which has the button
@app.route('/json')
def json():
    return render_template('index.html')

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print ("Hello")
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




if __name__ == '__main__':
    app.run("0.0.0.0",3000)
