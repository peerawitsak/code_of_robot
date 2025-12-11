from constant import *

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
        
        with open(file_path, 'a+') as file:
            file.write(f"senval = {SenVal} position ={self.position} ,back senval = {BackSenval} position = {self.Backposition}\n")
            
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

########################### main control #################################

    def Track_forward(self,mod_speed=0):#เดินไปข้างหน้าด้วยการ tag แบบ pid
        self.update()
        print(self.position)#######
        print(self.Backposition)####
        pwm_b.ChangeDutyCycle(self.rightspeed+mod_speed)
        GPIO.output(front_right,1) 
        GPIO.output(back_right,0)
        pwm_a.ChangeDutyCycle(self.leftspeed+mod_speed)
        GPIO.output(front_left,1)
        GPIO.output(back_left,0)
        time.sleep(0.05)

    def Track_backward(self,mod_speed=0):#ส่งค่าความเร็วขวาซ้ายสลับกัน
        self.update()
        print(self.position)#######
        print(self.Backposition)####
        pwm_b.ChangeDutyCycle(self.leftspeed+mod_speed)
        GPIO.output(front_right,0) 
        GPIO.output(back_right,1)
        pwm_a.ChangeDutyCycle(self.rightspeed+mod_speed)
        GPIO.output(front_left,0)
        GPIO.output(back_left,1)
        time.sleep(0.05)
        
    def motor_stop(self):#หยุดการทำงาน motor
        self.update()
        pwm_b.ChangeDutyCycle(0)
        GPIO.output(front_right,0) 
        GPIO.output(back_right,0)
        pwm_a.ChangeDutyCycle(0)
        GPIO.output(front_left,0)
        GPIO.output(back_left,0)
        time.sleep(0.05)
    
    def Turn_Right(self,speed=30):
        while self.Backposition != 3:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,0) 
            GPIO.output(back_right,1)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,1)
            GPIO.output(back_left,0)
            time.sleep(0.05)
            
        while self.Backposition != 4:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,0) 
            GPIO.output(back_right,1)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,1)
            GPIO.output(back_left,0)
            time.sleep(0.05)
            
        self.motor_stop()
    
    def Turn_Left(self,speed=30):
        while self.Backposition != 2:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,1) 
            GPIO.output(back_right,0)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,0)
            GPIO.output(back_left,1)
            time.sleep(0.05)
            
        while self.Backposition != 4:
            self.update()
            pwm_a.ChangeDutyCycle(speed)
            GPIO.output(front_right,1) 
            GPIO.output(back_right,0)
            pwm_b.ChangeDutyCycle(speed)
            GPIO.output(front_left,0)
            GPIO.output(back_left,1)
            time.sleep(0.05)
            
        self.motor_stop()
        
    def UTurn(self,speed=30):
        self.Turn_Right()
        self.Turn_Right()
        
################################# function #################################################
    
    def Backward_Until_black(self,i,mod_speed=0):
        while self.Backposition != i:
            self.Track_backward(mod_speed)
        while self.Backposition == i:
            self.Track_backward(mod_speed)

    def Forward_Until_Black(self,i,mod_speed=0):#เดินหน้าจนกว่าจะเจอเส้นดำ 1;ทั้งเส้น 2;ดำขวา 3;ดำซ้าย 
        while self.black_line != i : # หยุดตอนเจอ เส้นดำ 1ครั้ง
            self.Track_forward(mod_speed)
        while self.black_line == i :# เดินจนกว่าจะไม่เจอเส้น
            self.Track_forward(mod_speed)
    
    def Start_TO_Box(self):#วิ่งจากstartไปเก็บกล่อง
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น

    def Box_To_Left(self):#วิ่งหลังจากเก็บกล่องแล้วไปทางซ้าย
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Turn_left()
        self.Forward_Until_Black(2)#เจอเส้นดำขวา
        self.Turn_Right()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 

    def Box_To_Right(self):#วิ่งหลังจากเก็บกล่องแล้วไปทางขวา
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Turn_Right()
        self.Forward_Until_Black(3) #เจอเส้นดำซ้าย
        self.Turn_left()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 

    def Box_To_Mid(self):#วิ่งหลังจากเก็บกล่องแล้วตรงไปขึ้นสะพาน
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        #สำหรับขึ้นสะพาน
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        
    def Left_TO_Right(self):#วิ่งจากซ้ายหลังวางกล่องแล้วไปขวา
        self.UTurn()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(3)#เจอเส้นซ้าย
        self.Turn_Left()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(3)#เจอเส้นซ้าย
        self.Turn_Left()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 

    def Right_TO_Left(self):#วิ่งจากขวาหลังวางกล่องแล้วไปซ้าย
        self.UTurn()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(2)#เจอเส้นซ้าย
        self.Turn_Right()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(2)#เจอเส้นซ้าย
        self.Turn_Right()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 

    def Left_To_Start(self):#วิ่งจากซ้ายกลับไปจุดstart
        self.UTurn()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(3)#เจอเส้นซ้าย
        self.Turn_Left()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Turn_Right()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น

    def Right_To_Start(self):#วิ่งจากขวากลับไปจุดstart
        self.UTurn()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Forward_Until_Black(2)#เจอเส้นซ้าย
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 
        self.Turn_Right()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น
        self.Turn_Left()
        self.Forward_Until_Black(1)#เจอเส้นดำทั้งเส้น 



    # rb = Robot(Kp,Ki,Kd,Speed,Target) #สร้าง object ไปแล้วใน set up 







