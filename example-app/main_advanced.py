from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import sp
from plyer import gravity
from flash import Flash as flash #Workaround flash.py
import kivy_garden.speedmeter
from telemetrix import telemetrix
from math import atan2, degrees, tan, radians
import os

# Change if necessary
#IS_Android = True 
serial_port = '/dev/ttyUSB1'
serial_ip = 'localhost'
serial_ip_port = 8080

IS_ANDROID = os.path.exists('/system') and os.path.exists('/data')
print("IS_Android: ", IS_ANDROID)

CB_VALUE = 2

# Arduino Pins
ECHO_PIN = 5                    
TRIG_PIN = 4

#LEDs showing angle
PIN_R = 10
PIN_G = 8

DISTANCE_VPIN = 10 # virtual pin for distance
TORCH_APP_BTN_VPIN = 21 #virtual pin for app torch button
LED_STATE_VPIN = 22 #virtual pin for torch LED state (on/off)
BRIGHTNESS_VPIN = 23 #virtual pin for torch LED brightness

class Main(App):
    board = None
    distance = 0
    btn_connect = None
    FONT_SIZE = sp(20)
    torch_state_on = False
    brightness = 128
    has_gravity = False

    def connect(self, button):
        try: 
            if IS_ANDROID:
                self.board = telemetrix.Telemetrix(ip_address = serial_ip, ip_port = serial_ip_port)
            else:
                self.board = telemetrix.Telemetrix(com_port = serial_port)
        except Exception:
            Logger.warning("MyApp: Cannot communicate to Arduino")
            return

        #self.board.set_pin_mode_sonar(TRIG_PIN, ECHO_PIN, self.sonar_callback)
        self.board.set_pin_mode_analog_input(DISTANCE_VPIN, callback= self.sonar_callback)
        self.board.set_pin_mode_digital_input(LED_STATE_VPIN, self.on_led_state_change)
        self.board.set_pin_mode_digital_output(TORCH_APP_BTN_VPIN)
    
        self.board.set_pin_mode_analog_output(BRIGHTNESS_VPIN)
        self.board.set_pin_mode_digital_output(PIN_R)
        self.board.set_pin_mode_digital_output(PIN_G)

        self.root.ids.box1.remove_widget(button)

    def on_led_state_change(self, data): #Called when state of torch LED changes
        print("data: ", data)
        self.torch_state_on = data[CB_VALUE]
        if self.torch_state_on:
            flash.on()
        else:
            flash.off()
        self.root.ids.btn_light.state = 'down' if self.torch_state_on else 'normal'  #Adapt torch button state of app
            
    def on_torch_btn(self, obj): #Called when Torch button of app is pressed
        print("obj.state: ", obj.state)
        if obj.state == 'down':
            flash.on()
            if self.board is not None:
                self.board.digital_write(TORCH_APP_BTN_VPIN, 1)
            self.torch_state_on = True
        else:
            flash.off()
            if self.board is not None:
                self.board.digital_write(TORCH_APP_BTN_VPIN, 0)
            self.torch_state_on = False

    def on_brt_sldr(self, obj): #Called when brightness slider is moved
        if self.board is not None and self.torch_state_on == True:
            self.board.analog_write(BRIGHTNESS_VPIN, int(obj.value))
        self.brightness = int(obj.value)

    # Update SpeedMeter widget and label
    def update_meter(self, dt):
        self.root.ids.meter_widget.value = self.distance
        self.root.ids.meter_widget.label = f"{round(self.distance)} cm"
    
    # Called by OS every 100 milliseconds
    def update_angle(self, dt):
        x = y = 1
        max_angle = self.root.ids.sldr_angle.max
        min_angle = self.root.ids.sldr_angle.min
        # If gravity sensor is available, get coordinates
        if self.has_gravity == True:
            x, y, z = gravity.gravity
        else:
            # If no gravity sensor, get y value from slider, which can be changed by user in this case
            # This is useful for testing on a device without a gravity sensor
            angle = self.root.ids.sldr_angle.value
            y = tan(radians(angle))    

        # Calculate angle from x and y values
        if x is not None and y is not None:
            angle = round(degrees(atan2(y, x)), 1)
            # Update angle label
            self.root.ids.lbl_angle.text = f"Angle: {angle}°"
            # Ensure angle stays within slider range
            if angle > max_angle:
                angle = max_angle 
            if angle < min_angle:
                angle = min_angle 

            # Do the following only if angle has changed
            if hasattr(self, 'last_angle') and self.last_angle == angle:
                return

            self.last_angle = angle
            if self.board is not None:
                if -1 <= angle <= 1:
                    self.board.digital_write(PIN_G, 1)
                    self.board.digital_write(PIN_R, 0)
                else:
                    self.board.digital_write(PIN_G, 0)
                    self.board.digital_write(PIN_R, 1)

            # Update slider widget with new angle
            self.root.ids.sldr_angle.value = angle

    # Retrieves sonar distance
    def sonar_callback(self, data):
        self.distance = data[CB_VALUE]
        if self.distance > self.root.ids.meter_widget.max:
            self.distance = self.root.ids.meter_widget.max 
        Clock.schedule_once(self.update_meter) #Update meter widget
        
    def on_start(self):
        Logger.debug("MyApp: -->on_start()")
        self.has_serial = True
        meter_widget = self.root.ids.meter_widget
        try: 
            gravity.enable()
            self.has_gravity = True
        except NotImplementedError:
            Logger.warning("MyApp: No gravity sensor found")

        if self.has_gravity:
            Logger.info("MyApp: Gravity sensor ok")

        Clock.schedule_interval(self.update_angle, 0.1)

    def build(self):
        self.btn_connect = self.root.ids.btn_connect
        Logger.debug("MyApp: -->build()")
       #Window.size = (1110, 540)  # Example size

    def on_stop(self):
        Logger.debug("MyApp: -->on_stop()")
        if self.board is not None:
            self.board.shutdown()

if __name__ == '__main__':
    Main().run()
