from ClassMain import *

#----------------------------setup-------------------------------------#

GPIO.setmode(GPIO.BCM)#mode of set pin 
#GPIO.setmode(GPIO.Board)

#set sensor
GPIO.setup(sen1,GPIO.IN)
GPIO.setup(sen2,GPIO.IN)
GPIO.setup(sen3,GPIO.IN)
GPIO.setup(sen4,GPIO.IN)
GPIO.setup(sen5,GPIO.IN)
GPIO.setup(sen6,GPIO.IN)
GPIO.setup(sen7,GPIO.IN)
GPIO.setup(sen8,GPIO.IN)

GPIO.setup(sen9,GPIO.IN)
GPIO.setup(sen10,GPIO.IN)

GPIO.setup(button,GPIO.IN)

GPIO.setwarnings(False)

GPIO.setup(front_right,GPIO.OUT)
GPIO.setup(front_left,GPIO.OUT)
GPIO.setup(back_right,GPIO.OUT)
GPIO.setup(back_left,GPIO.OUT)

GPIO.setup(pwm_a,GPIO.OUT)
GPIO.setup(pwm_b,GPIO.OUT)

pwm_a = GPIO.PWM(pwm_a,1000) # forward (pin,frequency)
pwm_b = GPIO.PWM(pwm_b,1000) # backward (pin,frequency)

pwm_a.start(0) #start with 0% dutycycle
pwm_b.start(0) #start with 0% dutycycle

rb = Robot(Kp,Ki,Kd,Speed,Target)
#--------------------------function ---------------------------------

def Forward_Until_Black(i,mod_speed=0):#เดินหน้าจนกว่าจะเจอเส้นดำ 1;ทั้งเส้น 2;ดำขวา 3;ดำซ้าย 
    while rb.black_line != i : # หยุดตอนเจอ เส้นดำ 1ครั้ง
        rb.Track_forward(mod_speed)
    while rb.black_line == i :# เดินจนกว่าจะไม่เจอเส้น
        rb.Track_forward(mod_speed)
    
def Start_TO_Box():#วิ่งจากstartไปเก็บกล่อง
     Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
     Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น

def Box_To_Left():#วิ่งหลังจากเก็บกล่องแล้วไปทางซ้าย
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    rb.Turn_left()
    Forward_Until_Black(2)#เจอเส้นดำขวา
    rb.Turn_Right()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 

def Box_To_Right():#วิ่งหลังจากเก็บกล่องแล้วไปทางขวา
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    rb.Turn_Right()
    Forward_Until_Black(3) #เจอเส้นดำซ้าย
    rb.Turn_left()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 

def Box_To_Mid():#วิ่งหลังจากเก็บกล่องแล้วตรงไปขึ้นสะพาน
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    #สำหรับขึ้นสะพาน
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    
def Left_TO_Right():#วิ่งจากซ้ายหลังวางกล่องแล้วไปขวา
    rb.UTurn()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(3)#เจอเส้นซ้าย
    rb.Turn_Left()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(3)#เจอเส้นซ้าย
    rb.Turn_Left()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 

def Right_TO_Left():#วิ่งจากขวาหลังวางกล่องแล้วไปซ้าย
    rb.UTurn()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(2)#เจอเส้นซ้าย
    rb.Turn_Right()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(2)#เจอเส้นซ้าย
    rb.Turn_Right()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 

def Left_To_Start():#วิ่งจากซ้ายกลับไปจุดstart
    rb.UTurn()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(3)#เจอเส้นซ้าย
    rb.Turn_Left()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    rb.Turn_Right()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น

def Right_To_Start():#วิ่งจากขวากลับไปจุดstart
    rb.UTurn()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
    Forward_Until_Black(2)#เจอเส้นซ้าย
    rb.Turn_Right()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น
    rb.Turn_Left()
    Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 

