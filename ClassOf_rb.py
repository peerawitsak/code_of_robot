from constan import *

import RPi.GPIO as GPIO
import pigpio as pig
import time 

#----------------------------------function ----------------------------------------

############################# การคำนวณ ###############################
class Robot():
    def __init__(self,kp,ki,kd,Speed,target):
        self.position = None
        self.black_line = None
        
        self.Backposition = None
        
        self._error = None
        self.pid_value = None
        self.leftspeed = None
        self.rightspeed = None
        
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.Speed = Speed
        self.target = target
        
        self.previous_T = pig.pi().get_current_tick()
        self.Integral_error = 0
        self.previous_error = 0
        
    """อ่านค่า ส่งค่อออกเป็นposition 1 - 15 and 0 ถ้าไ่ม่เจอ 
    เช็คเส้นดำ out 1:เส้นดำทั้งเส้น 2:เส้นดำขวา 3:เส้นดำซ้าย 4:เจอเส้นดำตรงกลางเฉยๆ and 0 ถ้าไม่เจอ 
    """
    def update(self):
        BackSenval = [0,0]
        SenVal = [0,0,0,0,0,0,0,0]
        SenVal[0]=GPIO.input(sen1)
        SenVal[1]=GPIO.input(sen2)
        SenVal[2]=GPIO.input(sen3)
        SenVal[3]=GPIO.input(sen4)
        SenVal[4]=GPIO.input(sen5)
        SenVal[5]=GPIO.input(sen6)
        SenVal[6]=GPIO.input(sen7)
        SenVal[7]=GPIO.input(sen8)
        
        BackSenval[0]=GPIO.input(sen9)
        BackSenval[1]=GPIO.input(sen10)
        
        self.position = patterns.get(tuple(SenVal),0)
        self.black_line = patterns_black_line.get(tuple(SenVal),0)
        self.Backposition = patterns_Back.get(tuple(BackSenval),4)
        
        self._error = self.position-self.target
        
        self.PID_cal()
    # คำนวณ PID vale # x = error ; error = position - target
    def PID_cal(self):
        current_T = pig.pi().get_current_tick()
        delta_T  =(current_T-self.previous_T)/ 1.0e6
        self.previous_T = current_T

        P = self._error
        I = self.Integral_error + (self._error*delta_T)
        D = (self._error-self.previous_error)/delta_T if delta_T > 0 else 1 # จริง if condition else ไม่จริง // กัน หารด้วย 0

        self.pid_value = (self.Kp*P)+(self.Ki*I)+(self.Kd*D)
        
        self.Integral_error = I
        self.previous_error = self._error
        
        self.Motor_Control()
    #ทำการปรับจูนค่าความเร็ว motor ซ้ายขวา 
    def Motor_Control(self):
        right_speed_motor = self.Speed + self.pid_value
        left_speed_motor = self.Speed - self.pid_value
        
        if(right_speed_motor>100):
            right_speed_motor = 100
        elif(right_speed_motor<0):
            right_speed_motor=1
        
        if(left_speed_motor>100):
            left_speed_motor = 100
        elif(left_speed_motor<0):
            left_speed_motor =1
        
        self.leftspeed = left_speed_motor
        self.rightspeed = right_speed_motor

    def Track_forward(self,left,right):#เดินไปข้างหน้าด้วยการ tag แบบ pid
        self.update()
        pwm_b.ChangeDutyCycle(self.rightspeed+right)
        GPIO.output(front_right,1) 
        GPIO.output(back_right,0)
        pwm_a.ChangeDutyCycle(self.leftspeed+left)
        GPIO.output(front_left,1)
        GPIO.output(back_left,0)

    def Track_backward(self,left,right):#ส่งค่าความเร็วขวาซ้ายสลับกัน
        self.update()
        pwm_b.ChangeDutyCycle(self.leftspeed+left)
        GPIO.output(front_right,0) 
        GPIO.output(back_right,1)
        pwm_a.ChangeDutyCycle(self.rightspeed+right)
        GPIO.output(front_left,0)
        GPIO.output(back_left,1)
        
    def motor_stop(self):#หยุดการทำงาน motor
        self.update()
        pwm_b.ChangeDutyCycle(0)
        GPIO.output(front_right,0) 
        GPIO.output(back_right,0)
        pwm_a.ChangeDutyCycle(0)
        GPIO.output(front_left,0)
        GPIO.output(back_left,0)
    
    def Turn_Right(self,speed):
        while self.Backposition != 2:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,0) 
            GPIO.output(back_right,1)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,1)
            GPIO.output(back_left,0)
        while self.Backposition != 3:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,0) 
            GPIO.output(back_right,1)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,1)
            GPIO.output(back_left,0)
        self.motor_stop()
    
    def Turn_Left(self,speed):
        while self.Backposition != 1:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,1) 
            GPIO.output(back_right,0)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,0)
            GPIO.output(back_left,1)
        while self.Backposition != 3:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,1) 
            GPIO.output(back_right,0)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,0)
            GPIO.output(back_left,1)
        self.motor_stop()
        
    def UTurn(self,speed):
        while self.Backposition != 2:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,0) 
            GPIO.output(back_right,1)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,1)
            GPIO.output(back_left,0)
        while self.Backposition != 3:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,0) 
            GPIO.output(back_right,1)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,1)
            GPIO.output(back_left,0)
        while self.Backposition != 2:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,0) 
            GPIO.output(back_right,1)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,1)
            GPIO.output(back_left,0)
        while self.Backposition != 3:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,0) 
            GPIO.output(back_right,1)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,1)
            GPIO.output(back_left,0)
        self.motor_stop()
    

# rb = Robot(Kp,Ki,Kd,Speed,Target) #สร้าง object


######################## การเดินหลัก ######################
"""
def Forward_Until_Black(i,leftspeed,rightspeed):#เดินหน้าจนกว่าจะเจอเส้นดำ 1;ทั้งเส้น 2;ดำขวา 3;ดำซ้าย 
    while rb.black_line != i : # หยุดตอนเจอ เส้นดำ 1ครั้ง
        rb.Track_forward(leftspeed,rightspeed)
    while rb.black_line == i :# เดินจนกว่าจะไม่เจอเส้น
        rb.Track_forward(leftspeed,rightspeed)
    # time.sleep(Time_delay)
    #delay ให้ เกินเส้นดำ
    
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
"""




