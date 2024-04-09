import os
import time
import json
import subprocess
import base64
import ut803
import socket
import sys
import config_exp
import cv2

from PIL import Image
from PIL import ImageOps

from c_x_lab import weblab, redis

from labdiscoverylib import weblab_user


"""
This module is just an example of how you could organize your code. Here you would
manage any code related to your hardware, for example.

"""
@weblab.on_start
def start(client_data, server_data):
    print("************************************************************************")
    print("Preparing laboratory for user {}...".format(weblab_user.username))
    print()
    print(" - Typically, here you prepare resources.")
    print(" - Since this method is run *before* the user goes to the lab, you can't")
    print("   store information on Flask's 'session'. But you can store it on:")
    print("   weblab_user.data")
    weblab_user.data['local_identifier'] = weblab.create_token()
    print("   In this case: {}".format(weblab_user.data['local_identifier']))
    print()
    print("************************************************************************")
    


    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"img_home")
    data = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data
    sock.close()


@weblab.on_dispose
def dispose():
    print("************************************************************************")
    print("Cleaning up laboratory for user {}...".format(weblab_user.username))
    print()
    print(" - Typically, here you clean up resources (stop motors, delete programs,")
    print("   etc.)")
    print(" - In this example, we'll 'empty' the microcontroller (in a database)")
    print(" - Testing weblab_user.data: {}".format(weblab_user.data['local_identifier']))
    print()
    print("************************************************************************")

    """ The user exited (or the time slot finished). Clean resources. """
    p7 = subprocess.call( [config_exp.prog_default], shell=True)
    default_img = Image.open(config_exp.upld_jpg_default_path)
    default_img.save(config_exp.upld_jpg_path)
    #print 'default image restored on server'
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "img_copy"'
    sock.send(b"img_copy")
    data = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data
    sock.close()

     # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "switch00"'
    sock.send(b"switch00")
    data0 = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data0
    sock.close()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "switch10"'
    sock.send(b"switch10")
    data1 = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data1
    sock.close()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "switch20"'
    sock.send(b"switch20")
    data2 = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data2
    sock.close()

    # Jump to first picture on raspi

    #p8 = subprocess.call( ["rm", "-f", config.output_jpg_path])
    #print "Default status restored"

    #print "User left"

    return "{}"

    clean_resources()

def clean_resources():
    """
    This code could be in dispose(). However, since we want to call this low-level
    code from outside any request and we can't (since we're using
    weblab_user.username in dispose())... we separate it. This way, this code can
    be called from outside using 'flask clean-resources'
    """

@weblab.task()
def program_device(code):

    if weblab_user.time_left < 30:
        print("************************************************************************")
        print("Error: typically, programming the device takes around 10 seconds. So if ")
        print("the user has less than 10 secons to use the laboratory, don't start ")
        print("this task. Otherwise, the user session will still wait until the task")
        print("finishes, delaying the time assigned by the administrator")
        print("************************************************************************")
        return {
            'success': False,
            'reason': "Too few time"
        }

    print("************************************************************************")
    print("You decided that you wanted to program the robot, and for some reason,  ")
    print("this takes time. In labdiscoverylib, you can create a 'task': something that  ")
    print("you can start, and it will be running in a different thread. In this ")
    print("case, this is lasting for 10 seconds from now ")
    print("************************************************************************")
    if redis.get('hardware:fpga') == 'programming':
        # Just in case two programs are sent at the very same time
        return {
            'success': False,
            'reason': "Already programming"
        }
        
    else:
        p1 = subprocess.call( [config_exp.prog_file], shell=True)
        redis.set('hardware:fpga', 'programming')
        print("Still programming...")
        #print "Feedback:", p1
        if p1 == 0:
            return "Done"
        else:
            return "An Error (%s) occured!! Please be sure to chose the appropriate bit-file" % p1
""" 

    if code == 'division-by-zero':
        print("************************************************************************")
        print("Oh no! It was a division-by-zero code! Expect an error!")
        print("************************************************************************")
        redis.set('hardware:microcontroller', 'failed')
        10 / 0 # Force an exception to be raised

 
 
    print("************************************************************************")
    print("Yay! the robot has been programmed! Now you can retrieve the result ")
    print("************************************************************************")
    redis.set('hardware:microcontroller', 'programmed')

    return {
        'success': True 
    }"""

def send_file_to_device(self, file_content, file_info):
    """ A file, encoded in BASE64, has been sent. Do something with it """

    #print "File received:", file_info
    if file_info == "bit_file.sof":
        bitfile = open(config_exp.prog_file_path,'wb')
        content = base64.b64decode(file_content)
        bitfile.write(content)
        bitfile.close()
        return "Your bit file is transfered..."
    elif file_info == "upload_image.jpg":
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        #print 'connecting to %s port %s' % config_exp.server_address
        sock.connect(config_exp.server_address)

        jpgfile = open(config_exp.upld_jpg_path,'wb')
        content = base64.b64decode(file_content)
        jpgfile.write(content)
        jpgfile.close()
        #print 'file saved on server'
        try:
            img = Image.open(config_exp.upld_jpg_path)
            #print 'File format is: %s' %img.format
            if (img.format == 'JPEG') or (img.format == 'MPO'):
                new_img = ImageOps.fit(img, (1280,720), method=0, bleed=0.0, centering=(0.5, 0.5))
                new_img.save(config_exp.upld_jpg_path)
                jpg_file = 1
            else:
                new_img = Image.open(config_exp.upld_jpg_error_path)
                new_img.save(config_exp.upld_jpg_path)
                jpg_file = 0
                #print 'Wrong file format'
        except IOError:
            #print 'No image file'
            new_img = Image.open(config_exp.upld_jpg_error_path)
            new_img.save(config_exp.upld_jpg_path)
            jpg_file = 0
            #print 'Wrong file format'
        time.sleep(1)
        sock.send("img_upld")
        #print 'send "img_upld" to pi'
        time.sleep(1)
        com_data = sock.recv(8)
        time.sleep(1)
        #print 'received command from pi "%s"' % com_data
        time.sleep(1)
        #print 'send image "%s" to pi' %file_info
        f = open(config_exp.upld_jpg_path,'rb')
        #print 'File opened'
        l = f.read(1024)
        while (l):
            sock.send(l)
            #print '1024 bits sent'
            l = f.read(1024)
            #print 'read next 1024 bits'
        #print 'file sent'
        f.close()
        sock.close()

        #print 'send file "%s" to pi' % file_info

        if (jpg_file):
            return "Image upload successful!"
        return "Sorry, wrong image file format! See the FAQ for further information"

@weblab.task()
def gen_frames():
    camera = cv2.VideoCapture(-1)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@weblab.task()
def measure():
        core_current = ut803.measure_value()
        time.sleep(1)
        return "%s mA" % core_current

@weblab.task()
def program_invert():
    p1 = subprocess.call( [config_exp.prog_invert], shell=True)
    if p1 == 0:
        return "Done"
    else:
        return "An Error (%s) occured!! Please contact the administrator of the lab" % p1

@weblab.task()
def program_filter():
    p2 = subprocess.call( [config_exp.prog_filter], shell=True)
    if p2 == 0:
        return "Done"
    else:
        return "An Error (%s) occured!! Please contact the administrator of the lab" % p2

@weblab.task()
def program_edge():
    p3 = subprocess.call( [config_exp.prog_edge], shell=True)
    if p3 == 0:
        return "Done"
    else:
        return "An Error (%s) occured!! Please contact the administrator of the lab" % p3

@weblab.task()
def image_home():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"img_home")
    data = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data
    sock.close()
    return "command received %s" % data

@weblab.task()
def image_last():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"img_last")
    data = sock.recv(8)
    time.sleep(0.5)
    #print 'received command from pi "%s"' % data
    sock.close()
    return "command received %s" % data

    
@weblab.task()
def image_next():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"img_next")
    #print 'sent data'
    data = sock.recv(8)
    time.sleep(0.5)
    #print 'received command from pi "%s"' % data
    sock.close()
    return "command received %s" % data


@weblab.task()
def image_end():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"img_end_")
    data = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data
    sock.close()
    return "command received %s" % data 


@weblab.task()
def sw0_off():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"switch00")
    data = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data
    sock.close()
    return "command received %s" % data

@weblab.task()
def sw0_on():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"switch01")
    data = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data
    sock.close()
    return "command received %s" % data

@weblab.task()
def sw1_off():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"switch10")
    data = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data
    sock.close()
    return "command received %s" % data

@weblab.task()
def sw1_on():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"switch11")
    data = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data
    sock.close()
    return "command received %s" % data

@weblab.task()
def sw2_off():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"switch20")
    data = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data
    sock.close()
    return "command received %s" % data

@weblab.task()
def sw2_on():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    #print 'connecting to %s port %s' % config_exp.server_address
    sock.connect(config_exp.server_address)
    #print 'send command to pi "%s"' % command
    sock.send(b"switch21")
    data = sock.recv(8)
    time.sleep(1)
    #print 'received command from pi "%s"' % data
    sock.close()
    return "command received %s" % data   