这是基于树莓派和亚博四驱车套件的一个自定义版本，主要是把控制方式重新实现了一下。

// install mjpg-streamer

// install flask

vi /etc/rc.local
// add below

# run mjpg-streamer
LD_LIBRARY_PATH=/home/pi/4wd/mjpg-streamer/mjpg-streamer-experimental mjpg_streamer -i "input_uvc.so" -o "output_http.so -w /home/pi/4wd/mjpg-streamer/mjpg-streamer-experimental/www" &

# main 4wd control, andyyin's extension
python /home/pi/4wd/flask/index.py &


