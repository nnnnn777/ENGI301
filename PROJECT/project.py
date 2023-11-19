"""
--------------------------------------------------------------------------
Project Driver
--------------------------------------------------------------------------
License:   
Copyright 2023 <Nate>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

Project Driver for PocketBeagle

Software API:

"""
import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
from servo import Servo
from button import Button
from led import LED

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

SG90_FREQ               = 50                  # 20ms period (50Hz)
SG90_POL                = 0                   # Rising Edge polarity
SG90_MIN_DUTY           = 5                   # 1ms pulse (5% duty cycle)  -- Fully clockwise (right)
SG90_MAX_DUTY           = 10                  # 2ms pulse (10% duty cycle) -- Fully anti-clockwise (left)

# ------------------------------------------------------------------------
# Functions / Classes
# ------------------------------------------------------------------------

# Project
# Servo
# Button
# LED

# ------------------------------------------------------------------------
# Main Script
# ------------------------------------------------------------------------



class Project():
  def __init__(self, StopButton = "P2_2", CounterButton = "P2_33", ClockButton = "P2_35", servo = "P1_36", ledred = "P2_4", ledyellow = "P2_6", ledgreen = "P2_8", ledblue = "P2_10"): #initialization of pins
    self.reset_time = None # Creating instances of classes and initializing variables
    self.StopButton    = Button(StopButton)
    self.CounterButton = Button(CounterButton)
    self.ClockButton   = Button(ClockButton)
    self.servo = Servo(servo)
    self.position = 0
    self.ledred = LED(ledred)
    self.ledyellow = LED(ledyellow)
    self.ledgreen = LED(ledgreen)
    self.ledblue = LED(ledblue)
  
  def turn_servo_clockwise(self): # defining turn_servo_clockwise and changing the positional value, only can go from 0 to 100 with these parameters
    print("Move clockwise")
    if self.position < 100:
      self.position = self.position+25
      self.servo.turn(self.position)
  
  def turn_servo_counterclockwise(self): # defining turn_servo_counterclockwise
    print("Move counterclockwise")
    if self.position > 0:
      self.position = self.position-25
      self.servo.turn(self.position)
      
  def stop(self): # defining stoppage 
    print("Stopping the project.")
    self.cleanup()
    GPIO.cleanup()  # Cleanup GPIO resources
    exit()

  
  def run(self): # defining run, the project's active portion
    button_press_time  = 0.0      
    while True: # Essentially true as long as project is set up and connected to power
      # button_press_time = ClockButton.is_pressed()
      # if button_press_time < self.reset_time:
      if self.ClockButton.is_pressed():
          print("clock button pressed") # Both for clockwise and counterclockwise motion, the servo will turn upon the pressing of the designated buttons, but only throughout the set positional range, and the button cannot be mashed.
          self.turn_servo_clockwise()
          time.sleep(0.5)
      
      if self.CounterButton.is_pressed():
          print("counter button pressed")
          self.turn_servo_counterclockwise()
          time.sleep(0.5)
        # 
      time.sleep(0.1)
      
      # The code below turns the series of LEDs on and off depending on the value of position. The LED lightings will therefore correspond to the speed levels of the fan
      
      if self.position >= 0: # Red LED will always be on when code is running, and will be the only LED lit when the fan is off
        self.ledred.on()
      else:
        self.ledred.off()
        
      
      if self.position >= 25:
        self.ledyellow.on()
      else:
        self.ledyellow.off()
        
        
      if self.position >= 50:
        self.ledgreen.on()
      else:
        self.ledgreen.off()
      
      if self.position>= 75:
        self.ledblue.on()
      else:
        self.ledblue.off()
    

  def cleanup(self): #cleanup, servo reset.
    self.servo.cleanup()
  

if __name__ == "__main__":
    my_project = Project()
    try:
      my_project.run()
    except KeyboardInterrupt:
      my_project.cleanup()
      
        
