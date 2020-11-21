import serial
import time
from donkeycar.parts.controller import Joystick, JoystickController

class MyJoystick(Joystick):
    #An interface to a physical joystick available at /dev/input/js0
    def __init__(self, *args, **kwargs):
        super(MyJoystick, self).__init__(*args, **kwargs)

            
        self.button_names = {
            0x133 : 'X',
            0x134 : 'Y',
            0x131 : 'B',
            0x13b : 'start',
            0x13c : 'home',
            0x13a : 'select',
            0x13d : 'analog_left_button',
            0x13e : 'analog_right_button',
            0x136 : 'LB',
            0x137 : 'RB',
            0x130 : 'A',
        }


        self.axis_names = {
            0x0 : 'analog_left_horizontal',
            0x1 : 'analog_left_vertical',
            0x4 : 'analog_right_vertical',
            0x3 : 'analog_right_horizontal',
            0x10 : 'dpad_horizontal',
            0x11 : 'dpad_vertical',
            0x5 : 'RT',
            0x2 : 'LT',
        }



class MyJoystickController(JoystickController):
    #A Controller object that maps inputs to actions
    def __init__(self, *args, **kwargs):
        super(MyJoystickController, self).__init__(*args, **kwargs)


    def init_js(self):
        #attempt to init joystick
        try:
            self.js = MyJoystick(self.dev_fn)
            self.js.init()
        except FileNotFoundError:
            print(self.dev_fn, "not found.")
            self.js = None
        return self.js is not None


    def init_trigger_maps(self):
        #init set of mapping from buttons to function calls
            
        self.button_down_trigger_map = {
            'A' : self.toggle_mode,
            'X' : self.erase_last_N_records,
            'Y' : self.emergency_stop,
            'B' : self.toggle_manual_recording,
            'RB' : self.increase_max_throttle,
            'LB' : self.decrease_max_throttle,
            'start' : self.toggle_constant_throttle,
        }


        self.axis_trigger_map = {
            'analog_left_vertical' :  self.set_throttle,  
            'analog_right_horizontal' :  self.set_steering,
        }


# Display output `sudo screen /dev/ttyUSB0 115200`
class MySerialController:

    def __init__(self, *args, **kwargs):
        print("Starting My Serial Controller")

        self.angle = 0.0
        self.throttle = 0.0
        self.mode = 'user'
        self.recording = False
        self.serial = serial.Serial('/dev/ttyUSB0', 115200,
                                    timeout=1)  # Serial port - laptop: 'COM3', Arduino: '/dev/ttyACM0'

    def update(self):
        # delay on startup to avoid crashing
        print("Warming Serial Controller")
        time.sleep(3)

        while True:
            line = str(self.serial.readline().decode()).strip('\n').strip('\r')
            output = line.split()

            # steering
            if output[0].isnumeric() and float(output[0]) > 0:
                self.angle = (float(output[0]) - 1500) / 500
            
            # Throttle 
            if output[1].isnumeric() and float(output[0]) > 0:
                self.throttle = (float(output[1]) - 1500) / 500
                # if self.throttle > 0.01:
                # self.recording = True
                # print("Recording")
                # else:
                #    self.recording = False

            # Mode
            if len(output) > 2 and output[2].isnumeric():
                three_state = float(output[2])
                self.mode = 'user'
                if three_state >= 1000 and three_state < 1800:
                    self.mode = 'local_angle'
                if three_state >= 1800:
                    self.mode = 'local'

            # Recording
            #if len(output) > 2 and output[2].isnumeric():
            #    self.mode = 'user'
            #    if output[2] >= 1000 and output[2] < 1800:
            #        self.mode = 'local_angle'
            #    if output[2] >= 1800:
            #        self.mode = 'local'

            time.sleep(0.01)

    def run(self, img_arr=None):
        return self.run_threaded()

    def run_threaded(self, img_arr=None):
        # print("Signal:", self.angle, self.throttle)
        return self.angle, self.throttle, self.mode, self.recording