from machine import Pin, ADC, PWM, I2C
import time
import random
from time import sleep
import framebuf
from ssd1306 import SSD1306_I2C




# i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
# oled = SSD1306_I2C(128, 64, i2c)




##################################################################################
class LED:
    def __init__(self, color, pin):
        self.color = color
        self.pin = pin
        
    def Flash(self):
        self.pin.value(1)
        sleep(0.5)
        self.pin.value(0)
        sleep(0.25)
        
    def FlashAll(redLED, greenLED, yellowLED, blueLED, times):
        for i in range(times):
            redLED.pin.value(1)
            greenLED.pin.value(1)
            yellowLED.pin.value(1)
            blueLED.pin.value(1)
            sleep(0.5)
            redLED.pin.value(0)
            greenLED.pin.value(0)
            yellowLED.pin.value(0)
            blueLED.pin.value(0)
            sleep(0.25)
        
    def ResetAll(redLED, greenLED, yellowLED, blueLED):
        redLED.pin.value(0)
        greenLED.pin.value(0)
        yellowLED.pin.value(0)
        blueLED.pin.value(0)
        
        
class Button:
    def __init__(self, LED, pin):
        self.LED = LED
        self.pin = pin  
        
    def ButtonReader(self):
        if self.pin.value() == 1:
            while self.pin.value() == 1:
                self.LED.pin.value(1)
                sleep(0.25)
            self.LED.pin.value(0)
            return self
        return None
    
class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        
    def GameStart(self):
        self.pin.duty_u16(20000)
        self.pin.freq(196)
        sleep(0.5)
        self.pin.freq(147)
        sleep(0.15)
        
        self.pin.freq(196)
        sleep(0.5)
        self.pin.freq(147)
        sleep(0.15)
        
        self.pin.freq(196)
        sleep(0.15)
        self.pin.freq(147)
        sleep(0.15)
        self.pin.freq(196)
        sleep(0.15)
        self.pin.freq(220)
        sleep(0.15)
        self.pin.freq(294)
        sleep(0.6)
        
        self.pin.freq(262)
        sleep(0.5)
        self.pin.freq(220)
        sleep(0.15)
        self.pin.freq(262)
        sleep(0.5)
        self.pin.freq(220)
        sleep(0.15)
        self.pin.freq(262)
        sleep(0.15)
        self.pin.freq(220)
        sleep(0.15)
        self.pin.freq(185)
        sleep(0.15)
        self.pin.freq(220)
        sleep(0.15)
        self.pin.freq(147)
        sleep(0.6)
        
        
        self.pin.duty_u16(0)
        sleep(5)
        

######################################################################################

    
    
  
     
######################################################################################     


redLED = LED("red", Pin(18, Pin.OUT))
yellowLED = LED("yellow", Pin(19, Pin.OUT))
greenLED = LED("green", Pin(20, Pin.OUT))
blueLED = LED("blue", Pin(21, Pin.OUT))

COLORLIST = [redLED, greenLED, yellowLED, blueLED]

redButton = Button(redLED, Pin(13, Pin.IN, Pin.PULL_DOWN))
yellowButton = Button(yellowLED, Pin(12, Pin.IN, Pin.PULL_DOWN))
greenButton = Button(greenLED, Pin(11, Pin.IN, Pin.PULL_DOWN))
blueButton = Button(blueLED, Pin(10, Pin.IN, Pin.PULL_DOWN))

startButton = Button(None, Pin(14, Pin.IN, Pin.PULL_DOWN))

buzzer = Buzzer(PWM(Pin(22)))

# score variables
highScore = 0
currentScore = 0


# turn of LEDs
LED.ResetAll(redLED, yellowLED, greenLED, blueLED)
print("initialized")

# Main Loop
while True:
    # update high score
    if currentScore > highScore:
        highScore = currentScore
        
    #reset current score    
    currentScore = 0
    
    # display high score
#     oled.text(f"High Score: {highScore}", 0, 25)
#     oled.show()
    
    sequenceList = []
    gameOver = False

    if startButton.pin.value() == 1:
        print("game start")
        buzzer.GameStart()
        
        while True:
            
        
            outputList = []
            
            # Add random color to the sequence
            sequenceList.append(random.choice(COLORLIST))
            
            # display list
            for color in sequenceList:
                color.Flash()
            
            while len(sequenceList) > 0:
               
                redInput = redButton.ButtonReader()
                yellowInput = yellowButton.ButtonReader()
                greenInput = greenButton.ButtonReader()
                blueInput = blueButton.ButtonReader()
                
                if redInput != None  or yellowInput != None or greenInput != None or blueInput != None:
                    inputList = [redInput, yellowInput, greenInput, blueInput]
                    for button in inputList:
                        if button != None:
                            if button.LED == sequenceList[0]:
                                outputList.append(sequenceList.pop(0))
                                break
                            else:
                                gameOver = True
                                break
                if gameOver:
                    break
            
            if gameOver:
                LED.FlashAll(redLED, greenLED, yellowLED, blueLED, 3)
                break

            currentScore += 1
            
            sequenceList = outputList
            sleep(2)
                            
    
        
    
                


        
    