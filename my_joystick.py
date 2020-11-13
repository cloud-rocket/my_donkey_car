import serial
from donkeycar.parts.controller import Joystick, JoystickController
from donkeycar.parts.serial_controllrt import SerialController

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

class MySerialController(SerialController):

    def __init__(self, *args, **kwargs):
        print("Starting My Serial Controller")

        self.angle = 0.0
        self.throttle = 0.0
        self.mode = 'user'
        self.recording = False
        self.serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=1) #Serial port - laptop: 'COM3', Arduino: '/dev/ttyACM0'

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


