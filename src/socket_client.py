import socket
import threading
import queue
# Lab3 - Graphics

import sys, os
sys.path.insert(0, os.path.abspath('..'))

from common.core import BaseWidget, run
from common.gfxutil import topleft_label, CEllipse, KFAnim, AnimGroup

from kivy.core.window import Window
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics import Color, Ellipse, Rectangle, Line, Triangle
import numpy as np
# from kivy.graphics import PushMatrix, PopMatrix, Translate, Scale, Rotate
from kivy.clock import Clock as kivyClock

import numpy as np


class TriangleA(InstructionGroup):
    def __init__(self):
        super(TriangleA, self).__init__()

        # make the dot white
        self.add(Color(1,1,1))
        # self.center = np.array([100,100])
        # self.direction_vector = np.array([1,0])
        # self.triangle_size = 30
        # self.matrix = np.array([[-0.5, -np.sin(2*np.pi/3)],[-0.5, np.sin(2*np.pi/3)]])

        # self.body = Triangle([self.center+self.triangle_size*self.direction_vector,self.center+self.triangle_size*
        # self.direction_vector*self.matrix,self.center+self.triangle_size*self.direction_vector*self.matrix*self.matrix])
        # self.body = Triangle(points=[100,300,200,400,300,500])
        self.line = Line(points=(200,200,300,300), width=2)
        self.add(self.line)
        self.time = 0
        self.on_update(0)

    def on_update(self, dt):
        # print(client.recv(2048).decode(FORMAT))
        self.line.points = [200,200,received[0],received[1]]
        self.time += dt
        return True



class ExerciseWidget(BaseWidget):
    def __init__(self):
        super(ExerciseWidget, self).__init__()
        self.anim_group = AnimGroup()
        self.canvas.add(self.anim_group)
        self.line = TriangleA()
        self.anim_group.add(self.line)
        self.info = topleft_label()
        self.add_widget(self.info)
        self.last_touch = None

    def on_update(self):
        self.anim_group.on_update()
        self.update_info_label()

    def on_touch_down(self,touch):
        self.line.line.points=[200,200,touch.pos[0],touch.pos[1]]
        send(str((int(touch.pos[0]),int(touch.pos[1]))))


    def update_info_label(self):
        self.info.text = str(Window.mouse_pos)
        self.info.text += '\nfps:%d' % kivyClock.get_fps()
        self.info.text += '\nobjects:%d' % len(self.anim_group.objects)
        self.info.text += '\nreceived:' + str(received)



HEADER = 64
PORT = 11928
# PORT = 16835
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "192.168.1.26"
# SERVER = "LOCALHOST"
# SERVER = "3.134.125.175"
SERVER = "8.tcp.ngrok.io"
ADDR = (SERVER, PORT)
received = [0,0]
    

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
# client.setblocking(1)

def update_state(client,addr):
    run = True
    while run:
        
            # print(client.recv(2048).decode(FORMAT))
        msg = client.recv(2048).decode(FORMAT)
        # print(msg)
            # print(current_state)
        if msg:
            global received
            print(msg)
            received = eval(msg)
            print(received)
        else:
            send(DISCONNECT_MESSAGE)
            run = False
            # run = False

thread = threading.Thread(target=update_state, args=(client, ADDR))
thread.start()

def send(msg):
    # print(msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)



run(ExerciseWidget())
# thread.exit()
    # send("Hello World!")
    # input()
    # send("Hello Everyone!")
    # input()
    # send("Hello Tim!")

send(DISCONNECT_MESSAGE)